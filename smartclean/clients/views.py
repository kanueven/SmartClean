from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Client
from .serializers import ClientSerializer
from .permissions import IsOwnerOrAdminOrReadOnly

# Create your views here.
# a list of all clients and a new client create
class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        is_admin = user.is_superuser or user.groups.filter(name = 'admin').exists()
        if is_admin:
            return Client.objects.all()
        #client to only seee themselves
        return Client.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        is_admin = user.is_superuser or user.groups.filter(name='admin').exists()
        is_client = user.groups.filter(name='client').exists()

        if not (is_admin or is_client):
            raise PermissionDenied("Only clients or admins can create client profiles.")

        if is_client:
            serializer.save(user=user)
        else:
            serializer.save()

 # Retrieve / update / delete a single client
class ClientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminOrReadOnly]
    
    def update(self, request, *args, **kwargs):
        # Clients update their own profile, not delete others'
         kwargs['partial'] = True  
         return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        # Only admins can delete
        if not (request.user.is_superuser or request.user.groups.filter(name='admin').exists()):
            return Response(
                {'error': 'Only admins can delete client profiles.'},
                status=status.HTTP_403_FORBIDDEN
            )
        client = self.get_object()
        if not client.can_be_deleted():
            return Response(
                {'error': 'Cannot delete client with existing jobs.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        client.delete()
        return Response(
            {'message': f'Client {client.user.username} deleted successfully.'},
            status=status.HTTP_200_OK
        )
        
       