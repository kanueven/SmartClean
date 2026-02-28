from .serializers import ServiceSerializer,JobServiceSerializer
from .models import Service,JobService
from rest_framework import generics,permissions,status
from accounts.permissions import IsAdmin
from rest_framework.response import Response

# Create your views here.
class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.filter(is_active = True)
    serializer_class = ServiceSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [permissions.AllowAny()]

class ServiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [IsAdmin()]
    
    def update(self, request, *args, **kwargs):
        # Always allow partial updates so you only send changed fields
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        service = self.get_object()
        # Block deletion if service is used on any job
        if service.job_services.exists():
            return Response(
                {'error': 'Cannot delete a service that is attached to existing jobs. Deactivate it instead.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        service.delete()
        return Response(
            {'message': f'Service "{service.name}" deleted successfully.'},
            status=status.HTTP_200_OK
        )


class JobServiceListCreateView(generics.ListCreateAPIView):
    """List all services on a job, or add a service to a job."""
    serializer_class = JobServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        job_id = self.kwargs.get('job_id')
        return JobService.objects.filter(job_id=job_id).select_related('service')


class JobServiceDestroyView(generics.DestroyAPIView):
    """Remove a service from a job."""
    queryset = JobService.objects.all()
    serializer_class = JobServiceSerializer
    permission_classes = [IsAdmin]