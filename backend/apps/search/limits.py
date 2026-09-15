"""Daily Bedrock fresh-request quotas backed by Django's shared cache."""
from dataclasses import dataclass
from datetime import timedelta
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone


APP_LIMIT = getattr(settings, 'BEDROCK_APP_DAILY_LIMIT', 30)
USER_LIMIT = getattr(settings, 'BEDROCK_USER_DAILY_LIMIT', 5)
ANONYMOUS_LIMIT = getattr(settings, 'BEDROCK_ANONYMOUS_DAILY_LIMIT', 2)


@dataclass
class LimitDecision:
    allowed: bool
    message: str = ""
    app_key: str | None = None
    subject_key: str | None = None


def _key(kind: str, value: str) -> str:
    day = timezone.localdate().isoformat()
    return f"bedrock:daily:{day}:{kind}:{value}"


def _increment(key: str, limit: int) -> bool:
    try:
        if cache.add(key, 0, timeout=timedelta(days=2)):
            current = 0
        else:
            current = cache.get(key, 0)
        if current >= limit:
            return False
        cache.incr(key)
        return True
    except Exception:
        # Do not make search unavailable if the optional cache is down.
        return True


def reserve_bedrock_request(request) -> LimitDecision:
    """Reserve one fresh Bedrock call for the app and current subject."""
    app_key = _key("app", "all")
    if not _increment(app_key, APP_LIMIT):
        return LimitDecision(False, "AI limits reached for the day for the app; using deterministic fallback.")

    if request.user.is_authenticated:
        subject_key = _key("user", str(request.user.pk))
        if not _increment(subject_key, USER_LIMIT):
            try:
                cache.decr(app_key)
            except Exception:
                pass
            return LimitDecision(False, "AI limit reached for your account; using deterministic fallback.")
        return LimitDecision(True, app_key=app_key, subject_key=subject_key)

    if not request.session.session_key:
        request.session.create()
    subject_key = _key("session", request.session.session_key)
    if not _increment(subject_key, ANONYMOUS_LIMIT):
        try:
            cache.decr(app_key)
        except Exception:
            pass
        return LimitDecision(False, "Anonymous AI limit reached. Sign in to get more fresh AI searches; using deterministic fallback.")
    return LimitDecision(True, app_key=app_key, subject_key=subject_key)
