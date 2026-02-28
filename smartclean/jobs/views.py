from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied,ValidationError
from .models import Job
from .serializers import JobSerializer
from services.models import Service
from rest_framework.views import APIView
from decimal import Decimal

# Create your views here.

class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        is_admin = user.is_superuser or user.groups.filter(name='admin').exists()
        is_cleaner = user.groups.filter(name='cleaner').exists()
        queryset =Job.objects.all()
        
              # add filterimg by status
        status_param = self.request.query_params.get("status")
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        
        if is_admin:
            return queryset
        elif is_cleaner:
             # Cleaners see only jobs assigned to them
            return queryset.filter(cleaner__user=user)
        else:
            # Clients see only their own jobs
            return queryset.filter(client__user = user)
            

    def perform_create(self, serializer):
        user = self.request.user
        is_admin = user.is_superuser or user.groups.filter(name='admin').exists()
        is_client = user.groups.filter(name='client').exists()
        if not (is_client or is_admin):
            raise PermissionDenied("Onlyclients or admin can create jobs")
        # Link job to the client profile of the logged-in user
        if is_client:
                   serializer.save(client=self.request.user)
        else:
             # Admin must provide client in request body
            serializer.save()


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    def perform_destroy(self, instance):
        #  only draft jobs can be deleted
        if instance.status != "draft":
            raise ValidationError("Only draft jobs can be deleted.")
        instance.delete()

# Generate quote,admin can do this by summing prices
class GenerateQuoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request,pk):
        is_admin = request.user.is_superuser or request.user.groups.filter(name='admin').exists()
        if not is_admin:
            return Response( {"Only the admin can generate quotes"} 
                            ,status=status.HTTP_403_FORBIDDEN)
        job = get_object_or_404(Job,pk)
        
        if not job.can_transition("quoted"):
            return Response (
                {"error": "Invalid status transition"},
                status=status.HTTP_400_BAD_REQUEST
                )
            
        if not job.services.exists():
            return Response(
                {'error': 'Job has no services. Add services before generating a quote.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        total = jobs.calculate_total()
        job.quoted_price=Decimal(str(total))
        job.transition('quoted')
         
        return Response({ "message":"Quote generated",
                         "quoted_price":job.quoted_price},
                        'services':[
                {'name': s.name, 'price': s.base_price}
                for s in job.services.all()
            ])

# accept quote->client side
class AcceptQuoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)

        # Only the client who owns this job can accept

        if job.client.user != request.user:
            return Response(
                {"error": "Only job owner can accept quote"},
                status=status.HTTP_403_FORBIDDEN
            )

        if not job.can_transition("scheduled"):
            return Response(
                {'error': f'Cannot accept quote for a job with status "{job.status}".'},
                status=status.HTTP_400_BAD_REQUEST
            )
        job.quote_approved_at = timezone.now()
        job.save()
        job.transition("scheduled")

        return Response({
            'message': 'Quote accepted. Job is now scheduled.',
            'job_id': job.id,
            'status': job.status,
        })
        
# complete job->done by cleaner,they mark it as completed
class CompleteJobView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)

        if not job.cleaner or job.cleaner.user != request.user:
            return Response(
                {"error": "Only assigned cleaner can complete job"},
                status=status.HTTP_403_FORBIDDEN
            )

        if not job.can_transition("completed"):
            return Response(
                {'error': f'Cannot complete a job with status "{job.status}".'},
                status=status.HTTP_400_BAD_REQUEST
            )
        job.completed_at = timezone.now()
        job.final_price = job.quoted_price  # default final to quoted
        job.save()
        job.transition("completed")

        return Response({'message': 'Job marked as completed.',
            'job_id': job.id,
            'completed_at': job.completed_at,
            'final_price': job.final_price,})
        
class CancelJobView(APIView):
    """Admin or job owner can cancel a job."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        is_admin = request.user.is_superuser or request.user.groups.filter(name='admin').exists()
        is_owner = job.client.user == request.user

        if not (is_admin or is_owner):
            return Response(
                {'error': 'Only the job owner or admin can cancel a job.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if not job.can_transition('cancelled'):
            return Response(
                {'error': f'Cannot cancel a job with status "{job.status}".'},
                status=status.HTTP_400_BAD_REQUEST
            )
        reason = request.data.get('cancellation_reason', '')
        job.cancellation_reason = reason
        job.save()
        job.transition('cancelled')

        return Response({
            'message': 'Job cancelled.',
            'job_id': job.id,
            'cancellation_reason': job.cancellation_reason,
        })
class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def perform_destroy(self, instance):
        if instance.status != "draft":
            raise ValidationError("Only draft jobs can be deleted.")
        instance.delete()