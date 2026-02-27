from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # ROLE_CHOICES = (
    #     ('admin', 'Admin'),
    #     ('client', 'Client'),
    #     ('cleaner', 'Cleaner'),
    # )
    # role = models.CharField(max_length=10, choices=ROLE_CHOICES,default = 'client')

    def __str__(self):
        return f"{self.username} "
    @property
    def role(self):
            group = self.groups.first()
            return group.name if group else None