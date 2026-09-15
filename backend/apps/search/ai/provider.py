import json
import logging
import re
from typing import Optional
import httpx
from django.conf import settings
from .schemas import SearchPlan
from .prompts import SYSTEM_PROMPT, FEW_SHOT_EXAMPLES

logger = logging.getLogger(__name__)


def _bedrock_text(response) -> str:
    """Extract final text while tolerating GPT OSS reasoning content blocks."""
    blocks = response.get('output', {}).get('message', {}).get('content', [])
    text_blocks = [block.get('text') for block in blocks if isinstance(block, dict) and block.get('text')]
    if not text_blocks:
        raise ValueError(f"Bedrock response contained no text content: {response.get('output', {})}")
    return '\n'.join(text_blocks).strip()

class LLMProvider:
    def __init__(self):
        self.provider = getattr(settings, 'LLM_PROVIDER', 'bedrock')
        self.base_url = getattr(settings, 'LLM_BASE_URL', 'https://api.openai.com/v1').rstrip('/')
        self.api_key = getattr(settings, 'LLM_API_KEY', '').strip()
        self.model = getattr(settings, 'LLM_MODEL', 'openai.gpt-oss-20b-1:0')
        self.timeout = getattr(settings, 'LLM_TIMEOUT_SECONDS', 10.0)
        self.aws_region = getattr(settings, 'AWS_REGION', 'us-east-1')
        self.fallback_message = None

    @property
    def is_configured(self) -> bool:
        """Returns True only when an API key is provided and non-empty."""
        if self.provider == 'bedrock':
            # boto3 uses the standard AWS credential chain (environment, profile,
            # ECS/EC2 task role, or instance role). Do not require an API key.
            return True
        return bool(self.api_key)

    def parse_query(self, query: str) -> Optional[SearchPlan]:
        """
        Calls the OpenAI-compatible endpoint with the query.
        Returns validated SearchPlan on success, or None on failure/unconfigured.
        """
        if not self.is_configured:
            logger.info("LLM API key not configured. Using deterministic fallback.")
            return None

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for example in FEW_SHOT_EXAMPLES:
            messages.append({"role": "user", "content": example["query"]})
            messages.append({"role": "assistant", "content": json.dumps(example["output"])})
        messages.append({"role": "user", "content": query})

        if self.provider == 'bedrock':
            return self._parse_bedrock(messages, query)

        endpoint = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
        }

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(endpoint, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()

            raw_content = data['choices'][0]['message']['content'].strip()
            # Strip markdown code fences if model returned ```json ... ```
            raw_content = re.sub(r'^```(?:json)?\s*', '', raw_content)
            raw_content = re.sub(r'\s*```$', '', raw_content)

            parsed_json = json.loads(raw_content)
            parsed_json['query_text'] = query
            return SearchPlan(**parsed_json)

        except httpx.TimeoutException:
            self.fallback_message = "AI service timed out; using deterministic fallback."
            logger.warning("LLM request timed out after %.1f seconds. Falling back to rule parser.", self.timeout)
            return None
        except httpx.HTTPStatusError as exc:
            self.fallback_message = "AI service is unavailable; using deterministic fallback."
            logger.warning("LLM provider returned HTTP error %d: %s. Falling back.", exc.response.status_code, exc.response.text[:200])
            return None
        except (json.JSONDecodeError, KeyError, ValueError) as exc:
            self.fallback_message = "AI response was invalid; using deterministic fallback."
            logger.warning("Failed to parse or validate LLM response schema: %s. Falling back.", exc)
            return None
        except Exception as exc:
            self.fallback_message = "AI service is unavailable; using deterministic fallback."
            logger.error("Unexpected error in LLM provider adapter: %s. Falling back.", exc)
            return None

    def _parse_bedrock(self, messages, query: str) -> Optional[SearchPlan]:
        """Call Bedrock Converse using the ambient AWS credentials."""
        try:
            import boto3

            client = boto3.client('bedrock-runtime', region_name=self.aws_region)
            response = client.converse(
                modelId=self.model,
                system=[{"text": SYSTEM_PROMPT}],
                messages=[
                    {"role": message["role"], "content": [{"text": message["content"]}]}
                    for message in messages if message["role"] != "system"
                ],
                inferenceConfig={"temperature": 0.1, "maxTokens": 700},
            )
            raw_content = _bedrock_text(response)
            raw_content = re.sub(r'^```(?:json)?\s*', '', raw_content)
            raw_content = re.sub(r'\s*```$', '', raw_content)
            parsed_json = json.loads(raw_content)
            parsed_json['query_text'] = query
            return SearchPlan(**parsed_json)
        except Exception as exc:
            self.fallback_message = "AI service is unavailable; using deterministic fallback."
            logger.warning("Bedrock request failed; using deterministic fallback: %s", exc)
            return None
