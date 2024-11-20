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

        if not request.data.get("role"):
            request.data.set("role", "User")

        userregistrationserializer = UserRegistrationSerializer(data=request.data)
        userprofileSerializer = profileSerializer(data=request.data)

        if userregistrationserializer.is_valid() and userprofileSerializer.is_valid():
            try:
                userregistrationserializer.save()
                userprofileSerializer.save()
                return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
            except Exception as e:
                userregistrationserializer.delete()
                userprofileSerializer.delete()
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(userregistrationserializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login
class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Get the user's IP address
        ip_address = self.get_client_ip(request)
        print(f"Login attempt from IP: {ip_address}")  # Log the IP address

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user:
            # Generate refresh and access tokens using SimpleJWT
            refresh = RefreshToken.for_user(user)
            # loginTokens.objects.create(token=refresh.access_token, created_at=datetime.datetime.now(),
            #                                                 expiry=refresh.expires,
            #                                                 user_id=user.id)
            
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": f"Login successful from IP: {ip_address}"
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def get_client_ip(request):
        """Fetch the client IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', 'Unknown')
        return ip