from django.shortcuts import render
from rest_framework import generics
from .serializers import UserSerializer,RegisterUserSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import User

# Create your views here.
#regtration endpoint
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]
    
# List all users (admin only)
class ListUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # You can create a custom IsAdminUser permission

# Retrieve/update a single user
class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]