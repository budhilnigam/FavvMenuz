import logging
import time
from django.db import connection
from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health and readiness check verifying database and cache connectivity.
    Returns 200 when ready, 503 when critical services are unavailable.
    """
    start_time = time.time()
    checks = {
        'database': False,
        'cache': False,
    }

    # 1. Check Database Connectivity
    try:
        connection.ensure_connection()
        checks['database'] = True
    except Exception as exc:
        logger.error("Health check failed database verification: %s", exc)

    # 2. Check Cache Connectivity
    try:
        cache_key = '_healthz_ping_'
        cache.set(cache_key, 'pong', timeout=5)
        if cache.get(cache_key) == 'pong':
            checks['cache'] = True
    except Exception as exc:
        logger.warning("Health check cache check failed (cache is non-critical): %s", exc)

    duration_ms = round((time.time() - start_time) * 1000, 2)
    is_healthy = checks['database']

    response_data = {
        'status': 'healthy' if is_healthy else 'unhealthy',
        'checks': checks,
        'duration_ms': duration_ms,
        'service': 'favvmenuz-api',
    }

    status_code = status.HTTP_200_OK if is_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    return JsonResponse(response_data, status=status_code)
