from rest_framework import serializers
from .models import Cleaner

class CleanerSerializer(serializers.ModelSerializer):
    #cleaner info
    username = serializers.CharField(source = 'user.username',read_only = True)
    user_email = serializers.CharField(source ='user.email',read_only = True)
    
    class Meta:
        model = Cleaner
        fields = [
            'id', 'user', 'username', 'user_email', 
            'phone_number', 'address', 'skills', 'status', 
            'is_active', 'created_at', 'updated_at'
        ]
    read_only_fields = ['id', 'username', 'user_email', 'created_at', 'updated_at']
    
    # validate, and make sure status and is_active is valid
    def validate(self, value):
        if not value.is_active:
            raise serializers.ValidationError('This cleaner is inactive user')
        if hasattr(value, 'cleaner_profile'):
           raise serializers.ValidationError("This user already has a cleaner profile")
        return value
    # Validate status field to ensure it matches allowed choices
    def validate_status(self, value):
        allowed = [choice[0] for choice in Cleaner.STATUS_CHOICE]
        if value not in allowed:
            raise serializers.ValidationError(f"Status must be one of {allowed}")
        return value
    