from django.db import models
from accounts.models import User

# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE,related_name = 'client_profile')
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    special_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    
    def __str__(self):
        return f"{self.user.username}"

    
    