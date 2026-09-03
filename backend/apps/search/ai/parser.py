import re
from typing import List, Optional
from .schemas import SearchPlan, SUPPORTED_LOCALITIES

KNOWN_CUISINES = [
    "North Indian",
    "South Indian",
    "Chinese",
    "Italian",
    "Mughlai",
    "Street Food",
    "Healthy",
    "Continental",
    "Desserts",
    "Bakery",
    "Pan-Asian",
    "Punjabi",
    "Gujarati",
    "Mexican",
]

COMMON_FOOD_TERMS = [
    "paneer", "tikka", "dosa", "idli", "vada", "biryani", "noodles", "dim sum",
    "dumpling", "pizza", "pasta", "burger", "chaat", "dal", "makhani", "naan",
    "roti", "kulcha", "chole", "bhature", "pav bhaji", "gulab jamun", "rasmalai",
    "kulfi", "brownie", "coffee", "salad", "hummus", "falafel", "rice", "curd rice",
    "uttapam", "manchurian", "spring roll", "sandwich", "soup", "tandoori"
]

def parse_query_fallback(query: str) -> SearchPlan:
    """
    Deterministic rule-based query parser that extracts SearchPlan constraints
    when LLM is disabled or unavailable.
    """
    q_lower = query.lower()
    
    # 1. Price extraction
    # Patterns: under/below/less than/max/budget [of] [₹/rs/inr] [0-9]+
    max_price: Optional[float] = None
    min_price: Optional[float] = None

    max_price_match = re.search(
        r'(?:under|below|less\s+than|max|budget\s*(?:of)?|within)\s*(?:₹|rs\.?|inr)?\s*(\d+)',
        q_lower
    )
    if max_price_match:
        max_price = float(max_price_match.group(1))
    else:
        # Fallback: simple "₹350" or "350 rs"
        rupee_match = re.search(r'₹\s*(\d+)', query)
        if rupee_match:
            max_price = float(rupee_match.group(1))

    min_price_match = re.search(
        r'(?:above|over|more\s+than|min)\s*(?:₹|rs\.?|inr)?\s*(\d+)',
        q_lower
    )
    if min_price_match:
        min_price = float(min_price_match.group(1))

    # 2. Dietary extraction
    dietary_tags = []
    if re.search(r'\bjain\b', q_lower):
        dietary_tags.append('jain_friendly')
        dietary_tags.append('vegetarian')
    if re.search(r'\bveg\b|\bvegetarian\b', q_lower) and 'vegetarian' not in dietary_tags:
        dietary_tags.append('vegetarian')
    if re.search(r'\bvegan\b', q_lower):
        dietary_tags.append('vegan')
    if re.search(r'dairy[- ]free|without\s+dairy|no\s+milk', q_lower):
        dietary_tags.append('dairy_free')
    if re.search(r'gluten[- ]free|without\s+gluten', q_lower):
        dietary_tags.append('gluten_free')

    # 3. Excluded ingredients
    excluded_ingredients = []
    excluded_matches = re.findall(
        r'(?:without|no|exclude|excluding)\s+([a-zA-Z]+)',
        q_lower
    )
    for term in excluded_matches:
        if term not in ('oil', 'delay', 'doubt', 'spicy', 'sugar'):
            excluded_ingredients.append(term)
    if 'peanut' in q_lower or 'peanuts' in q_lower:
        if re.search(r'(?:without|no|free\s+from)\s+peanuts?', q_lower):
            if 'peanuts' not in excluded_ingredients:
                excluded_ingredients.append('peanuts')

    # If Jain, ensure onion and garlic are excluded conceptually
    if 'jain_friendly' in dietary_tags:
        if 'onion' not in excluded_ingredients:
            excluded_ingredients.append('onion')
        if 'garlic' not in excluded_ingredients:
            excluded_ingredients.append('garlic')

    # 4. Spice level
    spice_level = None
    if re.search(r'extra\s+spicy|very\s+spicy|fire', q_lower):
        spice_level = 'extra_spicy'
    elif re.search(r'\bspicy\b|hot', q_lower):
        spice_level = 'spicy'
    elif re.search(r'\bmild\b|less\s+spicy|not\s+too\s+spicy', q_lower):
        spice_level = 'mild'
    elif re.search(r'\bmedium\b', q_lower):
        spice_level = 'medium'

    # 5. Locality
    locality = None
    for loc in SUPPORTED_LOCALITIES:
        # Match "sector 62", "sec 62", "62"
        sec_num_match = re.search(r'sector\s*(\d+)', loc.lower())
        if sec_num_match:
            sec_num = sec_num_match.group(1)
            if re.search(rf'(?:sector|sec\.?)\s*{sec_num}\b', q_lower) or f" {sec_num} " in f" {q_lower} ":
                locality = loc
                break
        elif loc.lower() in q_lower:
            locality = loc
            break

    # 6. Distance
    max_distance_km = None
    distance_match = re.search(r'(?:within|under)\s*(\d+(?:\.\d+)?)\s*(?:km|kms|kilometer|kilometres)', q_lower)
    if distance_match:
        max_distance_km = float(distance_match.group(1))

    # 7. Cuisines
    cuisines = []
    for c in KNOWN_CUISINES:
        if c.lower() in q_lower:
            cuisines.append(c)

    # 8. Keywords
    keywords = []
    for food in COMMON_FOOD_TERMS:
        if food in q_lower and food not in excluded_ingredients:
            keywords.append(food)

    # 9. Sort preference
    sort_by = "relevance"
    if max_distance_km or "nearest" in q_lower or "closest" in q_lower:
        sort_by = "distance_asc"
    elif "cheapest" in q_lower or "affordable" in q_lower or "low price" in q_lower:
        sort_by = "price_asc"
    elif "top rated" in q_lower or "best" in q_lower or "highest rated" in q_lower:
        sort_by = "rating_desc"

    return SearchPlan(
        query_text=query,
        keywords=keywords,
        cuisines=cuisines,
        included_ingredients=[],
        excluded_ingredients=excluded_ingredients,
        dietary_tags=dietary_tags,
        min_price=min_price,
        max_price=max_price,
        spice_level=spice_level,
        locality=locality,
        max_distance_km=max_distance_km,
        sort_by=sort_by
    )
