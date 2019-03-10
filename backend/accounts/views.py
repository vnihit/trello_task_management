from django.shortcuts import render
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import api_view, permission_classes

# Create your views here.
User = get_user_model()

# handle local auth
class LocalAuth(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        """
        Create new users and tokens.
        """
        if User.objects.filter(username=request.data["username"]).exists():
            return Response(
                {"error": "Username is already being used"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.create_user(**request.data)
        long_term_token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": str(long_term_token),
                "email": user.email,
                "username": user.username,
                "name": f"{user.first_name} {user.last_name}",
                "success": "User creation successful",
            },
            status=status.HTTP_201_CREATED
        )

    
    def post(self, request, format=None):
        """
        Login existing users.
        """
        user = authenticate(**request.data)
        if not user:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        long_term_token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": str(long_term_token),
                "email": user.email,
                "username": user.username,
                "name": f"{user.first_name} {user.last_name}",
            },
            status=status.HTTP_200_OK
        )


@api_view(["GET"])
def test(APIView):
    return Response({"message": "Hello world"})
