from django.db import models

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# to hadle price per job and quantity,e.g. Job #1 has 2x Deep Clean + 1x Window Cleaning
class JobService(models.Model):
    job = models.ForeignKey(
        'jobs.Job',       
        on_delete=models.CASCADE,
        related_name='job_services'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='job_services'
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(
        max_digits=8, decimal_places=2,
        help_text='Snapshot of price at time of booking'
    )
    class Meta:
        # prevent same service added twice to same job
        unique_together = ('job', 'service')

    def __str__(self):
        return f"{self.quantity}x {self.service.name} on Job #{self.job.id}"

    @property
    def total_price(self):
        return self.quantity * self.unit_price