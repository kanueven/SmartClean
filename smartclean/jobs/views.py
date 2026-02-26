from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Job
from .serializers import JobSerializer
from services.models import Service
from rest_framework.views import APIView
from decimal import Decimal

# Create your views here.

class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    queryset =Job.objects.all()
   

    def get_queryset(self):
              # add filterimg
        status_param = self.request.query_params.get("status")
        if status_param:
            queryset = queryset.filter(status=status_param)
        user = self.request.user
        if user.role == "admin":
            return Job.objects.all()
        return Job.objects.filter(client=user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

# Generate quote,admin can do this
class GenerateQuoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request,pk):
        if request.user.role !="admin":
            return Response( {"Only the admin can generate quotes"}  ,status=status.HTTP_403_FORBIDDEN)
        
        job = get_object_or_404(Job,pk)
        if not job.can_transition("quoted"):
            return Response(
                {"error": "Invalid status transition"}, status=400 )
        
        total = sum(service.base_price for service in job.services.all())
        job.quoted_price=Decimal(total)
        job.transition('quoted')        
        return Response({ "message":"Quote generated","quoted_price":job.quoted_price})

# accept quote->client side
class AcceptQuoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)

        if job.client.user != request.user:
            return Response(
                {"error": "Only job owner can accept quote"},
                status=403
            )

        if not job.can_transition("scheduled"):
            return Response(
                {"error": "Invalid transition"},
                status=400
            )

        job.transition("scheduled")

        return Response({"message": "Quote accepted"})
# complete job->done by cleaner
class CompleteJobView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)

        if not job.cleaner or job.cleaner.user != request.user:
            return Response(
                {"error": "Only assigned cleaner can complete job"},
                status=403
            )

        if not job.can_transition("completed"):
            return Response(
                {"error": "Invalid transition"},
                status=400
            )

        job.transition("completed")

        return Response({"message": "Job completed"})
class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def perform_destroy(self, instance):
        if instance.status != "draft":
            raise ValidationError("Only draft jobs can be deleted.")
        instance.delete()