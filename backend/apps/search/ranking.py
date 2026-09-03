from typing import List, Dict, Any, Optional
from .ai.schemas import SearchPlan
from apps.catalog.models import MenuItem, Restaurant

def rank_and_explain_items(
    items: List[MenuItem],
    plan: SearchPlan,
    reference_coords: Optional[tuple[float, float]] = None,
    distance_map: Optional[Dict[int, float]] = None,
) -> List[Dict[str, Any]]:
    """
    Ranks filtered candidate items and computes grounded match explanations.
    Returns a sorted list of item result dictionaries.
    """
    results = []

    for item in items:
        score = 50.0  # Base score for passing hard filters
        reasons = []

        # 1. Keywords / Dish name match
        name_lower = item.name.lower()
        desc_lower = item.description.lower()
        for kw in plan.keywords:
            kw_l = kw.lower()
            if kw_l in name_lower:
                score += 30.0
                reasons.append(f"Dish matches '{kw}'")
                break
            elif kw_l in desc_lower or any(kw_l in ing.lower() for ing in item.ingredients):
                score += 15.0
                reasons.append(f"Contains '{kw}'")
                break

        # 2. Dietary Tag Matches
        for tag in plan.dietary_tags:
            if tag in item.dietary_tags:
                tag_label = tag.replace('_', ' ').title()
                score += 15.0
                reasons.append(f"Certified {tag_label}")

        # 3. Budget / Price Match
        if plan.max_price is not None:
            savings = plan.max_price - item.price_inr
            reasons.append(f"₹{item.price_inr:.0f} (Under your ₹{plan.max_price:.0f} budget)")
            score += min(15.0, max(0.0, (savings / plan.max_price) * 15.0))
        else:
            reasons.append(f"Priced at ₹{item.price_inr:.0f}")

        # 4. Spice Level Match
        if plan.spice_level and item.spice_level == plan.spice_level:
            score += 10.0
            reasons.append(f"Matches your '{plan.spice_level.replace('_', ' ').title()}' spice preference")

        # 5. Distance & Locality Match
        distance_km = None
        if distance_map and item.restaurant_id in distance_map:
            distance_km = distance_map[item.restaurant_id]
            reasons.append(f"{distance_km:.1f} km away in {item.restaurant.locality}")
            score += max(0.0, 20.0 - (distance_km * 2.0))
        elif plan.locality and item.restaurant.locality.lower() == plan.locality.lower():
            reasons.append(f"Located in requested locality ({item.restaurant.locality})")
            score += 15.0

        # 6. Restaurant Rating
        if item.restaurant.rating >= 4.5:
            score += 5.0
            reasons.append(f"High demo rating ({item.restaurant.rating} ★)")

        results.append({
            "item": item,
            "restaurant": item.restaurant,
            "relevance_score": round(score, 1),
            "match_reasons": reasons[:4],
            "distance_km": distance_km,
        })

    # Sort based on plan.sort_by
    if plan.sort_by == 'price_asc':
        results.sort(key=lambda r: r["item"].price_paise)
    elif plan.sort_by == 'price_desc':
        results.sort(key=lambda r: -r["item"].price_paise)
    elif plan.sort_by == 'rating_desc':
        results.sort(key=lambda r: -r["restaurant"].rating)
    elif plan.sort_by == 'distance_asc' and any(r["distance_km"] is not None for r in results):
        results.sort(key=lambda r: (r["distance_km"] if r["distance_km"] is not None else 999.0))
    else:
        # Default: relevance
        results.sort(key=lambda r: -r["relevance_score"])

    return results
