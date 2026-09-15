"""Generate explicitly synthetic catalog data with an AWS Bedrock model.

This is an opt-in development/demo command. The deterministic seed command
remains the recommended default for repeatable deployments and tests.
"""
import json
import random
import re
from typing import Any

import boto3
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from pydantic import BaseModel, Field, ValidationError

from apps.catalog.models import MenuItem, Restaurant
from apps.catalog.management.commands.seed_demo_data import LOCALITY_COORDINATES


def bedrock_text(response: dict) -> str:
    """Extract final text while tolerating GPT OSS reasoning content blocks."""
    blocks = response.get("output", {}).get("message", {}).get("content", [])
    text_blocks = [block.get("text") for block in blocks if isinstance(block, dict) and block.get("text")]
    if not text_blocks:
        raise ValueError(f"Bedrock response contained no text content: {response.get('output', {})}")
    return "\n".join(text_blocks).strip()


class GeneratedItem(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    category: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=10, max_length=600)
    price_inr: float = Field(gt=0, le=5000)
    ingredients: list[str] = Field(min_length=2, max_length=20)
    dietary_tags: list[str] = Field(default_factory=list)
    spice_level: str = "medium"
    allergens: list[str] = Field(default_factory=list)


class GeneratedRestaurant(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    description: str = Field(min_length=10, max_length=600)
    cuisines: list[str] = Field(min_length=1, max_length=4)
    price_band: str
    menu: list[GeneratedItem] = Field(min_length=1)


PROMPT = """You generate fictional restaurant catalog data for a software demo.
Everything must be invented: do not use real restaurant names, brands, addresses,
reviews, claims, or copied menu text. Return ONLY valid JSON, no markdown, with
this shape: {\"restaurants\":[{\"name\":string,\"description\":string,
\"cuisines\":[string],\"price_band\":\"₹\"|\"₹₹\"|\"₹₹₹\"|\"₹₹₹₹\",
\"menu\":[{\"name\":string,\"category\":string,\"description\":string,
\"price_inr\":number,\"ingredients\":[string],\"dietary_tags\":[string],
\"spice_level\":\"none\"|\"mild\"|\"medium\"|\"spicy\"|\"extra_spicy\",
\"allergens\":[string]}]}]}. Use only these dietary tags: vegetarian, vegan,
jain_friendly, dairy_free, gluten_free. Use varied regional Indian and global
cuisines, realistic INR prices, and make the menu internally consistent."""


class Command(BaseCommand):
    help = "Generate explicitly synthetic restaurants and menus using AWS Bedrock."

    def add_arguments(self, parser):
        parser.add_argument("--restaurants", type=int, default=8)
        parser.add_argument("--items-per-restaurant", type=int, default=10)
        parser.add_argument("--batch-size", type=int, default=4)
        parser.add_argument("--region", default=None)
        parser.add_argument("--model", default=None)
        parser.add_argument("--reset", action="store_true", help="Delete existing demo records first.")
        parser.add_argument("--seed", type=int, default=20261015)

    def handle(self, *args, **options):
        count = max(1, min(options["restaurants"], 100))
        per_restaurant = max(1, min(options["items_per_restaurant"], 30))
        batch_size = max(1, min(options["batch_size"], 10))
        region = options["region"] or settings.AWS_REGION
        model = options["model"] or settings.LLM_MODEL
        if not model.startswith("openai.gpt-oss"):
            self.stdout.write(self.style.WARNING(f"Using non-default Bedrock model: {model}"))

        if options["reset"]:
            MenuItem.objects.filter(is_demo=True).delete()
            Restaurant.objects.filter(is_demo=True).delete()

        client = boto3.client("bedrock-runtime", region_name=region)
        rng = random.Random(options["seed"])
        existing = set(Restaurant.objects.values_list("slug", flat=True))
        created_restaurants = created_items = 0

        for start in range(0, count, batch_size):
            requested = min(batch_size, count - start)
            user_prompt = (
                f"Create exactly {requested} restaurants, each with exactly {per_restaurant} menu items. "
                f"Use these synthetic Noida localities as themes: "
                f"{', '.join(rng.sample(list(LOCALITY_COORDINATES), k=min(requested, len(LOCALITY_COORDINATES))))}."
            )
            try:
                response = client.converse(
                    modelId=model,
                    system=[{"text": PROMPT}],
                    messages=[{"role": "user", "content": [{"text": user_prompt}]}],
                    inferenceConfig={"temperature": 0.8, "maxTokens": 12000},
                )
                text = bedrock_text(response)
                text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
                payload: Any = json.loads(text)
                generated = [GeneratedRestaurant.model_validate(x) for x in payload["restaurants"]]
            except Exception as exc:
                raise CommandError(f"Bedrock returned invalid seed data: {exc}") from exc

            for offset, data in enumerate(generated):
                locality = list(LOCALITY_COORDINATES)[(start + offset) % len(LOCALITY_COORDINATES)]
                base_lat, base_lng = LOCALITY_COORDINATES[locality]
                rest_slug = slugify(data.name)
                if not rest_slug or rest_slug in existing:
                    rest_slug = f"{rest_slug or 'synthetic-restaurant'}-{start + offset + 1}"
                existing.add(rest_slug)
                restaurant = Restaurant.objects.create(
                    name=data.name, slug=rest_slug, description=data.description,
                    cuisines=data.cuisines, locality=locality,
                    address=f"Synthetic Demo District, {locality}, Noida, UP",
                    latitude=round(base_lat + rng.uniform(-0.004, 0.004), 6),
                    longitude=round(base_lng + rng.uniform(-0.004, 0.004), 6),
                    price_band=data.price_band if data.price_band in {"₹", "₹₹", "₹₹₹", "₹₹₹₹"} else "₹₹",
                    rating=round(rng.uniform(3.8, 4.9), 1), review_count=rng.randint(20, 500),
                    image_asset="restaurant_default", is_demo=True,
                )
                created_restaurants += 1
                seen_items = set()
                for item in data.menu:
                    item_slug = slugify(item.name)
                    if not item_slug or item_slug in seen_items:
                        continue
                    seen_items.add(item_slug)
                    MenuItem.objects.create(
                        restaurant=restaurant, name=item.name, slug=item_slug,
                        category=item.category, description=item.description,
                        price_paise=round(item.price_inr * 100), ingredients=item.ingredients,
                        dietary_tags=item.dietary_tags, spice_level=item.spice_level,
                        allergen_info=item.allergens, image_asset="dish_default",
                        is_available=True, is_demo=True,
                    )
                    created_items += 1

        self.stdout.write(self.style.SUCCESS(
            f"Generated {created_restaurants} synthetic restaurants and {created_items} menu items with Bedrock."
        ))
