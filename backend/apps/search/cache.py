import hashlib
import json
import logging
from typing import Optional, Any
from django.core.cache import cache

logger = logging.getLogger(__name__)

def generate_cache_key(prefix: str, data: Any) -> str:
    """Generate MD5 hash cache key from string or json-serializable data."""
    if isinstance(data, str):
        payload = data.strip().lower()
    else:
        payload = json.dumps(data, sort_keys=True)
    hashed = hashlib.md5(payload.encode('utf-8')).hexdigest()
    return f"{prefix}:{hashed}"

def get_cached_search_plan(query: str) -> Optional[dict]:
    """Retrieve cached SearchPlan dict if present. Fails gracefully."""
    try:
        key = generate_cache_key("plan", query)
        cached = cache.get(key)
        if cached:
            logger.debug("Cache hit for SearchPlan: %s", query)
            return cached
    except Exception as exc:
        logger.warning("Cache get error (non-fatal): %s", exc)
    return None

def set_cached_search_plan(query: str, plan_dict: dict, timeout: int = 86400) -> None:
    """Cache SearchPlan dict. Fails gracefully."""
    try:
        key = generate_cache_key("plan", query)
        cache.set(key, plan_dict, timeout=timeout)
    except Exception as exc:
        logger.warning("Cache set error (non-fatal): %s", exc)

def get_cached_search_results(payload: dict) -> Optional[dict]:
    """Retrieve cached anonymous search response. Fails gracefully."""
    try:
        key = generate_cache_key("search_results", payload)
        return cache.get(key)
    except Exception as exc:
        logger.warning("Cache get error for search results: %s", exc)
    return None

def set_cached_search_results(payload: dict, results_dict: dict, timeout: int = 86400) -> None:
    """Cache static demo search results for 24 hours. Fails gracefully."""
    try:
        key = generate_cache_key("search_results", payload)
        cache.set(key, results_dict, timeout=timeout)
    except Exception as exc:
        logger.warning("Cache set error for search results: %s", exc)
