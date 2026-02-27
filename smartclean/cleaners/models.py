from django.db import models
from accounts.models import User

# Create your models here.
class Cleaner(models.Model):
    STATUS_CHOICE= (
        ('available','Available'),
         ('off_duty','Off Duty'),
          ('inactive','Inactive'),
        
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cleaner_profile'
    )
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    skills = models.TextField(blank=True,default = '',help_text='list of skills e.g. deep_clean,carpet,windows')
    status = models.CharField(max_length=20,choices=STATUS_CHOICE,default='available')
    is_active = models.BooleanField(default=True, help_text="Whether the cleaner is currently available")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} ({self.phone_number})"
    def can_be_deleted(self):
        """
        Will return False once jobs are linked.
        Hook: add `self.jobs.exists()` here when job app is ready.
        """
        return True