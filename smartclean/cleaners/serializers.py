from rest_framework import serializers
from .models import Cleaner


class CleanerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Cleaner
        fields = [
            'id', 'user', 'username', 'user_email',
            'phone_number', 'address', 'skills', 'status',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'username', 'user_email', 'created_at', 'updated_at']
        extra_kwargs = {
            'user': {'required': False}  #  cleaner doesn't need to send this,its frustating in the backend
        }

    def validate(self, attrs):
        request = self.context.get('request')

        # On update, skip creation checks
        if self.instance:
            return attrs

        user = attrs.get('user')
        is_admin = request.user.groups.filter(name='admin').exists()
        is_cleaner = request.user.groups.filter(name='cleaner').exists()

        if is_admin:
            # Admin must specify which user to create a profile for
            if not user:
                raise serializers.ValidationError("Admin must specify a user.")
            
            if not user.groups.filter(name='cleaner').exists():
                raise serializers.ValidationError("Cleaner must have 'cleaner' role.")

        elif is_cleaner:
            # Cleaner creates their own profile — ignore any 'user' field they sent
            attrs['user'] = request.user
            user = request.user
            if hasattr(user, 'cleaner_profile'):
                raise serializers.ValidationError("You already have a cleaner profile.")

        else:
            raise serializers.ValidationError("Only cleaners or admins can create cleaner profiles.")

        # Inactive user guard
        if user and not user.is_active:
            raise serializers.ValidationError("This user account is inactive.")

        # Final duplicate guard
        if user and Cleaner.objects.filter(user=user).exists():
            raise serializers.ValidationError("This user already has a cleaner profile.")

        return attrs

    def validate_status(self, value):
        allowed = [choice[0] for choice in Cleaner.STATUS_CHOICE]
        if value not in allowed:
            raise serializers.ValidationError(f"Status must be one of {allowed}.")
        return value