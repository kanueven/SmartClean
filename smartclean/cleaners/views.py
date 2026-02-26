from rest_framework import generics,filters
from .serializers import CleanerSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin
from .models import Cleaner

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
        # Admin sees all, regular users see only their own profile
        if self.request.user.is_staff:
            return Cleaner.objects.all()
        return Cleaner.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
         if 'user' not in serializer.validated_data:
            serializer.save(user=self.request.user)
         else:
            serializer.save()
class CleanerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cleaner.objects.all()
    serializer_class = CleanerSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]