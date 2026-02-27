from rest_framework import generics,filters,status
from .serializers import CleanerSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .permissions import IsOwnerOrAdmin
from rest_framework.exceptions import PermissionDenied
from .models import Cleaner
from rest_framework.response import Response

# Create your views here.
# Admins can create/update/delete cleaners
# Cleaners can only view/update their own profile
# List all cleaners / create a new cleaner (Admin only for POST)
class CleanerListCreateView(generics.ListCreateAPIView):
    serializer_class = CleanerSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['user__username', 'skills', 'status']
    filter_backends = [filters.SearchFilter]
    queryset = Cleaner.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        # Admin sees all, regular users see only their own profile
        if self.request.user.is_staff:
            return Cleaner.objects.all()
        return Cleaner.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        is_admin = user.groups.filter(name='admin').exists()
        is_cleaner = user.groups.filter(name='cleaner').exists()
        if not (is_admin or is_cleaner):
            raise PermissionDenied("Only admins or cleaners can create cleaner profiles.")
        # If cleaner, force-assign themselves regardless of what was sent
        if is_cleaner:
              serializer.save(user=user)
        else:
               serializer.save()
class CleanerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cleaner.objects.all()
    serializer_class = CleanerSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    #deleting a cleaner
    def destroy(self, request, *args, **kwargs):
        # Only admins can delete
        if not request.user.groups.filter(name='admin').exists():
            return Response(
                {'error': 'Only admins can delete cleaner profiles.'},
                status=status.HTTP_403_FORBIDDEN
            )
        cleaner = self.get_object()
        #  cleaner cannot be deleted if job exists
        if not cleaner.can_be_deleted():
            return Response(
                {'error': 'Cannot delete cleaner with existing jobs.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        cleaner.delete()
        return Response(
            {'message': f'Cleaner {cleaner.user.username} deleted successfully.'},
            status=status.HTTP_200_OK
        )
        # updating cleaner profile
        def update(self, request, *args, **kwargs):
        # Cleaners can only update their own profile, not delete others'
         kwargs['partial'] = True  # always allow partial updates (PATCH behaviour)
         return super().update(request, *args, **kwargs)