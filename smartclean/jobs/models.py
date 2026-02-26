from django.db import models
from cleaners.models import Cleaner
from clients.models import Client
from services.models import Service

# Create your models here.
class Job(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("quoted", "Quoted"),
        ("scheduled", "Scheduled"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
# jobs transition is it is drated->quoted->scheduled->canceled/inprogress, then completed
    ALLOWED_TRANSITIONS = {
    "draft": ["quoted", "cancelled"],
    "quoted": ["scheduled", "cancelled"],
    "scheduled": ["in_progress", "cancelled"],
    "in_progress": ["completed"],
    "completed": [],
    "cancelled": [],
}
    #relations
    client = models.ForeignKey(Client,on_delete=models.PROTECT,related_name='jobs')
    cleaner = models.ForeignKey(Cleaner,on_delete=models.SET_NULL,blank=True,related_name='jobs',null=True)
    services = models.ManyToManyField(Service)
    
    # job details
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        # Scheduling
    scheduled_date = models.DateTimeField(null=True, blank=True)
    # scheduled_time = models.TimeField(null=True, blank=True)
    estimated_duration_hours = models.DurationField(null=True,blank=True)
    actual_duration_hours = models.FloatField(null=True, blank=True)
    # Pricing (snapshot at quote time)
    quoted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Status & tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    quote_approved_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True, default='')

    # Feedback
    client_feedback = models.TextField(blank=True, default='')
    client_rating = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"job {self.id} -{self.status}"
    def can_transition(self,new_status):
        return new_status in self.ALLOWED_TRANSITIONS.get(self.status,[])
    def transition(self, new_status):
        if not self.can_transition(new_status):
                    raise ValueError(
            f"Cannot transition from {self.status} to {new_status}"
        )
        self.status = new_status
        self.save()