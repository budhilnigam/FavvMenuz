from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import status, views, permissions
from rest_framework.response import Response
from .serializers import UserSerializer, UserRegisterSerializer, FavoriteSerializer
from .services import get_user_favorites, toggle_favorite, delete_user_favorite

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CSRFTokenView(views.APIView):
    """
    Returns CSRF token and sets the csrftoken cookie for subsequent state-changing requests.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token = get_token(request)
        return Response({'csrftoken': token})


class RegisterView(views.APIView):
    """
    Registers a new user and starts an authenticated session.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    """
    Authenticates user credentials and starts an authenticated session.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'detail': 'Username and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                return Response({'detail': 'User account is disabled.'}, status=status.HTTP_403_FORBIDDEN)
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(
            {'detail': 'Invalid username or password.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(views.APIView):
    """
    Terminates the current session and flushes session data.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)


class MeView(views.APIView):
    """
    Returns current authenticated user details.
    """
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(UserSerializer(request.user).data)


class FavoriteListView(views.APIView):
    """
    List or create user favorites. Restricted strictly to the authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        favorites = get_user_favorites(request.user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        restaurant_id = request.data.get('restaurant')
        menu_item_id = request.data.get('menu_item')

        if not restaurant_id and not menu_item_id:
            return Response(
                {'detail': 'Provide either restaurant or menu_item ID.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        fav, created = toggle_favorite(
            user=request.user,
            restaurant_id=int(restaurant_id) if restaurant_id else None,
            menu_item_id=int(menu_item_id) if menu_item_id else None
        )

        if not created:
            return Response({'detail': 'Favorite removed.', 'favorited': False}, status=status.HTTP_200_OK)

        serializer = FavoriteSerializer(fav)
        return Response({'detail': 'Favorite added.', 'favorited': True, 'favorite': serializer.data}, status=status.HTTP_201_CREATED)


class FavoriteDetailView(views.APIView):
    """
    Remove a favorite by ID, preventing cross-user deletions.
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        deleted = delete_user_favorite(request.user, pk)
        if not deleted:
            return Response({'detail': 'Favorite not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'Favorite removed.'}, status=status.HTTP_204_NO_CONTENT)
