from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserTier  # Adjust the import based on your app structure

class SimpleAuthenticationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Try to authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)

        if user is not None:
            # User is authenticated; check for their tier
            try:
                user_tier = 2  # UserTier.objects.get(user=user).tier
                # Example of tier-based logic: restrict access for users below tier 1
                if user_tier == 0:
                    return Response({
                        "authentication": True,
                        "tier": user_tier,
                        "message": "Basic access granted"
                    })
                elif user_tier == 1:
                    return Response({
                        "authentication": True,
                        "tier": user_tier,
                        "message": "Standard access granted"
                    })
                elif user_tier == 2:
                    return Response({
                        "authentication": True,
                        "tier": user_tier,
                        "message": "Premium access granted"
                    })
                else:
                    return Response({
                        "authentication": False,
                        "error": "Unknown tier."
                    }, status=status.HTTP_403_FORBIDDEN)
            except UserTier.DoesNotExist:
                return Response({
                    "authentication": False,
                    "error": "User tier not set."
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            # Invalid credentials
            return Response({
                "authentication": False,
                "error": "Invalid username or password."
            }, status=status.HTTP_401_UNAUTHORIZED)


