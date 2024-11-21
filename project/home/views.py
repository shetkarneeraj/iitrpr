from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from datetime import datetime
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

class CoursesView(APIView):
    """
    View for fetching courses. Validates access token, refreshes if needed.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Extract tokens from headers
        authorization_header = request.headers.get("Authorization", "")
        refresh_token = request.headers.get("Refresh", None)

        if not authorization_header.startswith("Bearer "):
            return Response({"detail": "Authorization header missing or invalid."}, status=400)

        # Extract the access token
        access_token = authorization_header.split("Bearer ")[-1]
        new_access_token = None

        try:
            # Validate the access token
            validated_token = self.authentication_classes[0]().get_validated_token(access_token)
        except AuthenticationFailed:
            # Handle token expiration or invalidity
            if not refresh_token:
                return Response({"detail": "Access token expired. Refresh token missing."}, status=401)

            try:
                # Refresh the access token using the refresh token
                new_access_token = str(RefreshToken(refresh_token).access_token)
            except Exception as e:
                return Response({"detail": f"Unable to refresh token: {str(e)}"}, status=401)

        # Protected data (courses)
        courses = [
            {"id": 1, "name": "Django Basics"},
            {"id": 2, "name": "Advanced REST APIs"},
            {"id": 3, "name": "Machine Learning Fundamentals"},
        ]

        # Return courses along with a new access token if refreshed
        return Response(
            {
                "data": {"courses": courses},
                "auth": {"access_token": new_access_token if new_access_token else access_token},
            },
            status=200,
        )

@api_view(['GET', 'POST'])
def logout_view(request):
    return Response({'message': 'Logged out successfully.'})