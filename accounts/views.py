from django.shortcuts import render
from .serializers import UserSerializer,AdminCreateSerializer,Forgetpasswordserializer,ResetPasswordserializer
from .models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class UserSignupView(generics.CreateAPIView):
    serializer_class=UserSerializer
    permission_classes=[AllowAny]

class AdminSignupView(generics.CreateAPIView):
    serializer_class=AdminCreateSerializer
    permission_classes=[AllowAny]

class LoginView(TokenObtainPairView):
   

    """
    Takes email + password and returns access & refresh tokens
    """

# Refresh token
class RefreshTokenView(TokenRefreshView):
    pass

class Logoutview(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        try:
            refresh_token=request.data["refresh"]
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"},status=status.HTTP_200_OK)
        except KeyError:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        
class Forgetpassword(APIView):
    permission_classes=[AllowAny]
    serializer_class=Forgetpasswordserializer

    def post(self, request):
        ser = Forgetpasswordserializer(data=request.data)
        ser.is_valid(raise_exception=True)
        result = ser.save()                 # this is {"message": "..."}
        return Response(result, status=200) # DON'T use s
    
class Resetpassword(APIView):
    permission_classes=[AllowAny]
    serializer_class=ResetPasswordserializer

    def post(self, request):
        serializer = ResetPasswordserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()   # now create() is called
        return Response(result, status=200)
