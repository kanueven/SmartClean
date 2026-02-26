from django.db import models

# Create your models here.
class Job(models.Model):
    #relations
    client = models.ForeignKey(Client,on_delete=models.PROTECT,related_name='jobs')
    cleaner = models.ForeignKey(Cleaner,on_delete=models.SET_NULL,blank=True,related_name='jobs')
    
    # job details
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        # Scheduling
    scheduled_date = models.DateField(null=True, blank=True)
    scheduled_time = models.TimeField(null=True, blank=True)
    estimated_duration_hours = models.FloatField(null=True, blank=True)
    actual_duration_hours = models.FloatField(null=True, blank=True)
    # Pricing (snapshot at quote time)
    quoted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Status & tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_quote')
    quote_approved_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True, default='')

    # Feedback
    client_feedback = models.TextField(blank=True, default='')
    client_rating = models.PositiveIntegerField(null=True, blank=True)