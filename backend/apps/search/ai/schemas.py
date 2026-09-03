from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator

SUPPORTED_LOCALITIES = [
    'Sector 18',
    'Sector 62',
    'Sector 137',
    'Sector 50',
    'Sector 76',
    'Sector 104',
    'Noida Expressway',
    'Greater Noida West',
]

SUPPORTED_DIETARY_TAGS = [
    'vegetarian',
    'vegan',
    'jain_friendly',
    'dairy_free',
    'gluten_free',
]

SUPPORTED_SPICE_LEVELS = [
    'none',
    'mild',
    'medium',
    'spicy',
    'extra_spicy',
]

SUPPORTED_SORT_OPTIONS = [
    'relevance',
    'price_asc',
    'price_desc',
    'rating_desc',
    'distance_asc',
]

class SearchPlan(BaseModel):
    query_text: str = Field(default="", description="Original raw user query")
    keywords: List[str] = Field(default_factory=list, description="Target dish, food, or item keywords")
    cuisines: List[str] = Field(default_factory=list, description="Extracted cuisine labels")
    included_ingredients: List[str] = Field(default_factory=list, description="Ingredients requested")
    excluded_ingredients: List[str] = Field(default_factory=list, description="Ingredients or allergens to exclude")
    dietary_tags: List[str] = Field(default_factory=list, description="Dietary requirements")
    min_price: Optional[float] = Field(default=None, description="Minimum price in INR")
    max_price: Optional[float] = Field(default=None, description="Maximum price in INR")
    spice_level: Optional[str] = Field(default=None, description="Desired spice preference")
    locality: Optional[str] = Field(default=None, description="Target Noida locality")
    max_distance_km: Optional[float] = Field(default=None, description="Maximum distance radius in km")
    sort_by: str = Field(default="relevance", description="Sorting criteria")

    @field_validator('dietary_tags', mode='before')
    @classmethod
    def normalize_dietary_tags(cls, v):
        if not v:
            return []
        cleaned = []
        for tag in v:
            t = str(tag).strip().lower().replace('-', '_').replace(' ', '_')
            if 'jain' in t:
                cleaned.append('jain_friendly')
            elif t in ('veg', 'vegetarian'):
                cleaned.append('vegetarian')
            elif t == 'vegan':
                cleaned.append('vegan')
            elif 'dairy' in t and ('free' in t or 'without' in t):
                cleaned.append('dairy_free')
            elif 'gluten' in t and ('free' in t or 'without' in t):
                cleaned.append('gluten_free')
            elif t in SUPPORTED_DIETARY_TAGS:
                cleaned.append(t)
        return list(dict.fromkeys(cleaned))

    @field_validator('spice_level', mode='before')
    @classmethod
    def normalize_spice_level(cls, v):
        if not v:
            return None
        s = str(v).strip().lower().replace('-', '_').replace(' ', '_')
        if s in SUPPORTED_SPICE_LEVELS:
            return s
        if 'extra' in s or 'fire' in s or 'hot' in s:
            return 'extra_spicy'
        if 'spice' in s:
            return 'spicy'
        if 'mild' in s or 'less' in s or 'low' in s:
            return 'mild'
        if 'medium' in s or 'moderate' in s:
            return 'medium'
        if 'none' in s or 'not' in s:
            return 'none'
        return None

    @field_validator('locality', mode='before')
    @classmethod
    def normalize_locality(cls, v):
        if not v:
            return None
        v_str = str(v).strip()
        for loc in SUPPORTED_LOCALITIES:
            if loc.lower() == v_str.lower() or loc.lower().replace(' ', '') == v_str.lower().replace(' ', ''):
                return loc
            # e.g. "62" or "sec 62"
            if "62" in v_str and "62" in loc:
                return "Sector 62"
            if "18" in v_str and "18" in loc:
                return "Sector 18"
            if "137" in v_str and "137" in loc:
                return "Sector 137"
            if "50" in v_str and "50" in loc:
                return "Sector 50"
            if "76" in v_str and "76" in loc:
                return "Sector 76"
            if "104" in v_str and "104" in loc:
                return "Sector 104"
            if "expressway" in v_str.lower() and "Expressway" in loc:
                return "Noida Expressway"
            if "greater noida" in v_str.lower() or "noida west" in v_str.lower():
                return "Greater Noida West"
        return v_str

    @field_validator('min_price', 'max_price', mode='before')
    @classmethod
    def validate_prices(cls, v):
        if v is None or v == "":
            return None
        val = float(v)
        return max(0.0, val)

    @field_validator('max_distance_km', mode='before')
    @classmethod
    def validate_distance(cls, v):
        if v is None or v == "":
            return None
        val = float(v)
        return min(max(0.5, val), 50.0)
