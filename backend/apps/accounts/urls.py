from django.urls import path
from .views import CSRFTokenView, RegisterView, LoginView, LogoutView, MeView

urlpatterns = [
    path('csrf/', CSRFTokenView.as_view(), name='auth-csrf'),
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),
    path('me/', MeView.as_view(), name='auth-me'),
]
