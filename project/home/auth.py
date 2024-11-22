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
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework_simplejwt.tokens import AccessToken

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
    Handles user login and returns a single JWT access token.
    """

    def post(self, request):
        # Extract username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user:
            # Generate a JWT access token
            access_token = str(AccessToken.for_user(user))

            return Response({
                "access_token": access_token,
                "expires_in": 5 * 60 * 60,  # Expiration time in seconds (5 hours)
            }, status=200)

        return Response({"error": "Invalid credentials"}, status=HTTP_401_UNAUTHORIZED)
    """
    Handles user login and returns JWT tokens along with user role and client IP.
    """

    def post(self, request):
        # Extract username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Get the client's IP address
        ip_address = self.get_client_ip(request)
        print(f"Login attempt from IP: {ip_address}")  # Log the IP address for debugging

        # Authenticate the user
        user = authenticate(username=username, password=password)
        print(user)

        if user:
            try:
                # Fetch user profile for additional information
                profile = Profile.objects.get(username=user)
            except Profile.DoesNotExist:
                return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            authorization_header = (f"Bearer {str(refresh.access_token)}")
            print(authorization_header)

            return Response({
                "access": str(refresh.access_token),
                "role": profile.user_type,  # Replace with your Profile field for user role
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def get_client_ip(request):
        """
        Fetch the client IP address from the request headers or META data.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', 'Unknown')
        return ip