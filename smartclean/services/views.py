from .serializers import ServiceSerializer
from .models import Service
from rest_framework import generics,permissions

# Create your views here.
class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.filter(is_active = True)
    serializer_class = ServiceSerializer
    
    def get_permissions(self):
        if self.request.method =="POST":
            return [permissions.IsAdminUser()]
        
        return [permissions.IsAuthenticated()]

class ServiceUpdateView(generics.UpdateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAdminUser]