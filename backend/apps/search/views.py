from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .serializers import SearchRequestSerializer, SearchResponseSerializer
from .services import execute_search_pipeline

class SearchThrottle(AnonRateThrottle):
    scope = 'search'

class SearchView(APIView):
    """
    Search and discover dishes and restaurants using natural language or explicit filters.
    Supports both AI-interpreted and rule-based fallback queries.
    """
    permission_classes = [AllowAny]
    throttle_classes = [SearchThrottle, UserRateThrottle]

    def post(self, request):
        serializer = SearchRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        raw_query = data.get('query', '')
        explicit_filters = {
            'locality': data.get('locality'),
            'cuisines': data.get('cuisines', []),
            'dietary_tags': data.get('dietary_tags', []),
            'max_price': data.get('max_price'),
            'min_price': data.get('min_price'),
            'spice_level': data.get('spice_level'),
            'max_distance_km': data.get('max_distance_km'),
            'sort_by': data.get('sort_by', 'relevance'),
        }

        output = execute_search_pipeline(raw_query=raw_query, explicit_filters=explicit_filters, request=request)
        response_serializer = SearchResponseSerializer(output)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class SearchSuggestionsView(APIView):
    """
    Returns popular preset search suggestions for quick discovery.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        suggestions = [
            {
                "id": "s1",
                "label": "Spicy vegetarian under ₹350 near Sector 62",
                "query": "Show me spicy vegetarian dishes below ₹350 near Sector 62",
                "badge": "Popular",
                "icon": "Flame"
            },
            {
                "id": "s2",
                "label": "Crispy Dosa under ₹200",
                "query": "Crispy golden dosa under ₹200",
                "badge": "Budget",
                "icon": "Utensils"
            },
            {
                "id": "s3",
                "label": "Jain-friendly lunch near Sector 137",
                "query": "Show me Jain-friendly dinner options within 3 km of Sector 137",
                "badge": "Jain",
                "icon": "Sparkles"
            },
            {
                "id": "s4",
                "label": "Woodfired pizza in Sector 18",
                "query": "Woodfired Margherita Pizza under ₹500 in Sector 18",
                "badge": "Italian",
                "icon": "Pizza"
            },
            {
                "id": "s5",
                "label": "Healthy protein salad & bowls",
                "query": "Healthy quinoa avocado salad or bowls under ₹400",
                "badge": "Fitness",
                "icon": "Salad"
            },
            {
                "id": "s6",
                "label": "Desserts and kulfi under ₹150",
                "query": "Authentic Kulfi or warm Gulab Jamun under ₹150",
                "badge": "Sweet",
                "icon": "IceCream"
            }
        ]
        return Response(suggestions)
