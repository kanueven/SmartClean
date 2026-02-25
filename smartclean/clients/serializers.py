import django.db
from rest_framework import serializers
from .models import Client
from accounts.models import User

class ClientSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source = "user.email", read_only = True)
    username = serializers.CharField(source = "user.username", read_only = True)
    
    class Meta:
        model = Client
        fields = [ 'id', 'user', 'user_email', 'username', 'phone_number', 
                  'address', 'special_instructions', 'created_at', 'updated_at']
        read_only_fields = ['id','created_at','updated_at']
        
    # Before saving, let me check if this user is valid for this client profile
    def validate_user(self,value):
        if value.role != 'client':
            raise serializers.ValidationError("You must have be a client")
        # prevent duplicates
        if self.instance is None and hasattr(value,'client_profile'):
            raise serializers.ValidationError("You already have a profile")
        return value