from rest_framework.response import Response
from rest_framework import generics,status
from .serializers import UserSerializer,RegisterUserSerializer,AssignGroupSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from .models import User
from django.contrib.auth.models import Group
from .permissions import IsAdmin

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
    permission_classes = [IsAdminUser]

# Retrieve/update a single user
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Any authenticated user can view/edit their own profile. Admins can edit anyone."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        obj = super().get_object()
        # Only allow users to edit themselves unless they're admin
        if obj != self.request.user and not self.request.user.groups.filter(name='admin').exists():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only edit your own profile.")
        return obj
    
    def destroy(self, request, *args, **kwargs):
        # Only admins can delete users
        if not request.user.groups.filter(name='admin').exists():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only admins can delete users.")
        user = self.get_object()
        # Soft delete — never hard delete users from the DB
        user.is_active = False
        user.save()
        return Response(
            {'message': f'User {user.username} has been deactivated.'},
            status=status.HTTP_200_OK
        )

class AssignGroupView(APIView):
    """Admin can reassign a user's group after registration."""
    permission_classes = [IsAdmin]

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AssignGroupSerializer(data=request.data)
        if serializer.is_valid():
            new_group_name = serializer.validated_data['group']
            # Remove existing groups first so a user only ever has one role
            user.groups.clear()
            group, _ = Group.objects.get_or_create(name=new_group_name)
            user.groups.add(group)
            return Response({'message': f'{user.username} assigned to {new_group_name}.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)