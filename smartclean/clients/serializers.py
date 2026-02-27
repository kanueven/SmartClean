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
        extra_kwargs = {
            'user':{'required':False}
        }
        
    # Before saving, let me check if this user is valid for this client profile
    def validate(self, attrs):
        request = self.context.get('request')

        # Skip checks on update
        if self.instance:
            return attrs

        is_admin = request.user.is_superuser or request.user.groups.filter(name='admin').exists()
        is_client = request.user.groups.filter(name='client').exists()

        if is_admin:
            user = attrs.get('user')
            if not user:
                raise serializers.ValidationError("Admin must specify a user.")
            if not user.groups.filter(name='client').exists():
                raise serializers.ValidationError("The specified client must have 'client' role")
        elif is_client:
            # Auto assign themselves
            attrs['user'] = request.user
            user = request.user
            if Client.objects.filter(user=user).exists():
                raise serializers.ValidationError("You already have a client profile.")
        else:
            raise serializers.ValidationError("Only clients or admins can create client profiles.")

        # Inactive user guard
        user = attrs.get('user')
        if user and not user.is_active:
            raise serializers.ValidationError("This client account is inactive")

        return attrs