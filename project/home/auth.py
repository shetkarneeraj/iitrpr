from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, profileSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from home.models import Profile, loginTokens
import datetime
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny

def check_auth(request, reqRole):
    jwt_authenticator = JWTAuthentication()
    try:
        validated_token = jwt_authenticator.get_validated_token(request.headers.get('x-access-token'))
        user = jwt_authenticator.get_user(validated_token)
        role = Profile.objects.get(user=user).role
        return user, role in reqRole
    except AuthenticationFailed:
        return AnonymousUser(), 'Unauthorized'


# User Registration
class UserRegistrationView(APIView):
    def post(self, request):

        if not request.data.get("user_type"):
            request.data["user_type"] = "user"

        userregistrationserializer = UserRegistrationSerializer(data=request.data)
        userprofileSerializer = profileSerializer(data=request.data)

        if userregistrationserializer.is_valid() and userprofileSerializer.is_valid():
            try:
                userregistrationserializer.save()
                userprofileSerializer.save()
                return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(userregistrationserializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login
class UserLoginView(APIView):
    """
    Handles user login and provides role-based authentication.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]  # POST (login) is accessible to all, others require authentication.

    def get_permissions(self):
        """
        Overrides permissions based on the HTTP method.
        """
        if self.request.method == 'POST':
            return [AllowAny()]  # Allow anyone to access POST (login).
        return [IsAuthenticated()]  # Require authentication for other methods.

    # Get user list
    def get(self, request):
        """
        Returns the role of the authenticated user.
        """
        user = request.user
        if user.is_anonymous:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        user_profile = Profile.objects.get(username=user)

        try:
            required_roles = ['superadmin', 'admin', 'moderators']
            user_profiles = Profile.objects.filter(user_type__in=required_roles)  # Use filter() for multiple objects

            user_profiles_list = []
            for person in user_profiles:
                serialized_person = profileSerializer(person).data  # Serialize each profile
                user_profiles_list.append(serialized_person)

            return Response({"users": user_profiles_list}, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    # Login
    def post(self, request):
        """
        Handles user login and returns a JWT access token.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        # Get client IP address
        ip_address = self.get_client_ip(request)

        # Authenticate user
        user = authenticate(username=username, password=password)
        if user:
            try:
                # Fetch profile for role-based data
                profile = Profile.objects.get(username=user)
            except Profile.DoesNotExist:
                return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

            if profile.login == True:
                return Response({"error": "User already logged in"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            profile.last_ip = ip_address
            profile.login = True
            profile.save()

            return Response({
                "access": str(refresh.access_token),
                "role": profile.user_type,
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    # Logout
    def delete(self, request):
        """
        Logs out the user by blacklisting the refresh token.
        """
        try:
            # Fetch user profile
            user = request.user
            profile = Profile.objects.get(username=user)
            profile.login = False
            profile.last_ip = None
            profile.save()
            # Blacklist access token
            refresh_token = request.headers.get('Authorization').split(' ')[1]
            AccessToken(refresh_token).blacklist()
            return Response({"message": "User logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod
    def get_client_ip(request):
        """
        Fetches the client IP address.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', 'Unknown')
        return ip