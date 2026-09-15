from rest_framework import serializers
from apps.catalog.serializers import MenuItemSerializer, RestaurantSerializer

class SearchRequestSerializer(serializers.Serializer):
    query = serializers.CharField(required=False, allow_blank=True, default="")
    locality = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    cuisines = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    dietary_tags = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    max_price = serializers.FloatField(required=False, allow_null=True)
    min_price = serializers.FloatField(required=False, allow_null=True)
    spice_level = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    max_distance_km = serializers.FloatField(required=False, allow_null=True)
    sort_by = serializers.CharField(required=False, default="relevance")


class SearchPlanSerializer(serializers.Serializer):
    query_text = serializers.CharField(allow_blank=True)
    keywords = serializers.ListField(child=serializers.CharField())
    cuisines = serializers.ListField(child=serializers.CharField())
    included_ingredients = serializers.ListField(child=serializers.CharField())
    excluded_ingredients = serializers.ListField(child=serializers.CharField())
    dietary_tags = serializers.ListField(child=serializers.CharField())
    min_price = serializers.FloatField(allow_null=True)
    max_price = serializers.FloatField(allow_null=True)
    spice_level = serializers.CharField(allow_null=True)
    locality = serializers.CharField(allow_null=True)
    max_distance_km = serializers.FloatField(allow_null=True)
    sort_by = serializers.CharField()


class SearchResultItemSerializer(serializers.Serializer):
    item = MenuItemSerializer()
    restaurant = RestaurantSerializer()
    relevance_score = serializers.FloatField()
    match_reasons = serializers.ListField(child=serializers.CharField())
    distance_km = serializers.FloatField(allow_null=True)


class SearchResponseSerializer(serializers.Serializer):
    search_plan = SearchPlanSerializer()
    search_mode = serializers.ChoiceField(choices=['ai', 'fallback'])
    total_results = serializers.IntegerField()
    results = SearchResultItemSerializer(many=True)
    empty_suggestion = serializers.CharField(allow_null=True, allow_blank=True)
    ai_message = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    is_demo_data = serializers.BooleanField(default=True)
