import logging
from typing import Dict, Any, Tuple
from django.db.models import Q
from apps.catalog.models import MenuItem, Restaurant
from apps.catalog.management.commands.seed_demo_data import LOCALITY_COORDINATES
from .ai.schemas import SearchPlan
from .ai.provider import LLMProvider
from .ai.parser import parse_query_fallback
from .distance import haversine_distance_km
from .ranking import rank_and_explain_items
from .cache import (
    get_cached_search_plan,
    set_cached_search_plan,
    get_cached_search_results,
    set_cached_search_results,
)
from .limits import reserve_bedrock_request

logger = logging.getLogger(__name__)

def execute_search_pipeline(
    raw_query: str = "",
    explicit_filters: Dict[str, Any] = None,
    request=None,
) -> Dict[str, Any]:
    """
    Executes the full discovery search pipeline:
    1. Query interpretation (LLM -> Fallback)
    2. Explicit filter merging
    3. Hard constraint DB filtering
    4. Distance evaluation
    5. Deterministic ranking & explanation generation
    """
    if explicit_filters is None:
        explicit_filters = {}

    clean_query = raw_query.strip()
    cache_payload = {"query": clean_query.lower(), "filters": explicit_filters}
    cached_results = get_cached_search_results(cache_payload)
    if cached_results:
        logger.debug("Search response cache hit for query=%r", clean_query)
        return cached_results

    search_mode = 'fallback'
    ai_message = None
    cache_output = True
    cache_plan = True
    plan: SearchPlan

    # Check cache for search plan if clean_query is provided
    cached_plan_data = get_cached_search_plan(clean_query) if clean_query else None
    if cached_plan_data:
        plan = SearchPlan(**cached_plan_data)
        search_mode = cached_plan_data.get('_mode', 'fallback')
    else:
        # Step 1: LLM interpretation
        llm = LLMProvider()
        llm_plan = None
        if clean_query and llm.is_configured:
            if request is not None and llm.provider == 'bedrock':
                decision = reserve_bedrock_request(request)
            else:
                decision = None
            if decision is None or decision.allowed:
                llm_plan = llm.parse_query(clean_query)
                ai_message = llm.fallback_message
            else:
                ai_message = decision.message
                cache_output = decision.message.startswith('AI limits reached for the day for the app')
                cache_plan = False

        if llm_plan:
            plan = llm_plan
            search_mode = 'ai'
        elif clean_query:
            plan = parse_query_fallback(clean_query)
            search_mode = 'fallback'
        else:
            plan = SearchPlan(query_text="")
            search_mode = 'fallback'

        # Cache normalized plan
        if clean_query:
            plan_dict = plan.model_dump()
            plan_dict['_mode'] = search_mode
            if cache_plan and not ai_message:
                set_cached_search_plan(clean_query, plan_dict)

    # Step 2: Merge explicit UI overrides
    if explicit_filters.get('locality'):
        plan.locality = explicit_filters['locality']
    if explicit_filters.get('cuisines'):
        plan.cuisines = list(dict.fromkeys(plan.cuisines + explicit_filters['cuisines']))
    if explicit_filters.get('dietary_tags'):
        plan.dietary_tags = list(dict.fromkeys(plan.dietary_tags + explicit_filters['dietary_tags']))
    if explicit_filters.get('max_price') is not None:
        plan.max_price = float(explicit_filters['max_price'])
    if explicit_filters.get('min_price') is not None:
        plan.min_price = float(explicit_filters['min_price'])
    if explicit_filters.get('spice_level'):
        plan.spice_level = explicit_filters['spice_level']
    if explicit_filters.get('max_distance_km') is not None:
        plan.max_distance_km = float(explicit_filters['max_distance_km'])
    if explicit_filters.get('sort_by'):
        plan.sort_by = explicit_filters['sort_by']

    # Step 3: Database Query with Hard Constraints
    qs = MenuItem.objects.select_related('restaurant').filter(is_available=True)

    # Hard price filters
    if plan.max_price is not None:
        max_paise = int(plan.max_price * 100)
        qs = qs.filter(price_paise__lte=max_paise)
    if plan.min_price is not None:
        min_paise = int(plan.min_price * 100)
        qs = qs.filter(price_paise__gte=min_paise)

    # Hard dietary filters (must satisfy all specified tags)
    for tag in plan.dietary_tags:
        qs = qs.filter(dietary_tags__icontains=tag)

    # Excluded ingredients / allergens (hard exclusions)
    for excl in plan.excluded_ingredients:
        qs = qs.exclude(
            Q(ingredients__icontains=excl) |
            Q(allergen_info__icontains=excl)
        )

    # Locality filter (if locality specified without an explicit radius, restrict to that locality)
    if plan.locality and plan.max_distance_km is None:
        qs = qs.filter(restaurant__locality__iexact=plan.locality)

    # Cuisine filter (match restaurant cuisines or item category)
    if plan.cuisines:
        cuisine_q = Q()
        for c in plan.cuisines:
            cuisine_q |= Q(restaurant__cuisines__icontains=c) | Q(category__icontains=c)
        qs = qs.filter(cuisine_q)

    # Keywords filter (if keywords extracted, filter or prioritize)
    if plan.keywords:
        kw_q = Q()
        for kw in plan.keywords:
            kw_q |= Q(name__icontains=kw) | Q(description__icontains=kw) | Q(ingredients__icontains=kw)
        qs = qs.filter(kw_q)

    # Step 4: Geographic and Locality Calculations
    reference_coords = None
    distance_map: Dict[int, float] = {}

    if plan.locality:
        reference_coords = LOCALITY_COORDINATES.get(plan.locality)

    candidate_items = list(qs[:150])  # Bounded set for distance & ranking

    if reference_coords:
        ref_lat, ref_lng = reference_coords
        filtered_by_dist = []
        for item in candidate_items:
            rest = item.restaurant
            dist = haversine_distance_km(ref_lat, ref_lng, rest.latitude, rest.longitude)
            distance_map[rest.id] = dist
            if plan.max_distance_km is not None and dist > plan.max_distance_km:
                continue
            filtered_by_dist.append(item)
        candidate_items = filtered_by_dist

    # Step 5: Deterministic Ranking and Match Explanations
    ranked_results = rank_and_explain_items(
        items=candidate_items,
        plan=plan,
        reference_coords=reference_coords,
        distance_map=distance_map
    )

    # Step 6: Empty state suggestion
    empty_suggestion = None
    if len(ranked_results) == 0:
        suggestions = []
        if plan.max_price is not None and plan.max_price < 300:
            suggestions.append(f"Try increasing your budget above ₹{plan.max_price:.0f}")
        if plan.dietary_tags and 'jain_friendly' in plan.dietary_tags:
            suggestions.append("Check restaurants in Sector 137 or Sector 62 which offer dedicated Jain menus")
        if plan.locality:
            suggestions.append(f"Explore adjacent localities near {plan.locality}")
        if plan.max_distance_km:
            suggestions.append(f"Expand your distance radius beyond {plan.max_distance_km} km")
        if not suggestions:
            suggestions.append("Try broadening your keywords or removing some dietary exclusions")
        empty_suggestion = ". ".join(suggestions) + "."

    output = {
        "search_plan": plan.model_dump(),
        "search_mode": search_mode,
        "total_results": len(ranked_results),
        "results": ranked_results[:40],
        "empty_suggestion": empty_suggestion,
        "ai_message": ai_message,
        "is_demo_data": True,
    }
    if cache_output:
        set_cached_search_results(cache_payload, output)
    return output
