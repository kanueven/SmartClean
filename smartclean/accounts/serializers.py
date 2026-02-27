from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group

class RegisterUserSerializer(serializers.ModelSerializer):
    # write_only=True: The password fields will be accepted in requests but never included in responses
    # validators=[validate_password]: The password is checked against Django's password validation rules (e.g., minimum length, not too common). 
    # If it fails, the serializer will return a validation error automatically
    password = serializers.CharField(write_only = True,required = True,validators = [validate_password])
    password2 = serializers.CharField(write_only = True, required = True)
    role = serializers.ChoiceField(choices=["client","cleaner","admin"])
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email',  'password', 'password2','role']
        

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Your passwords should match')
        return attrs

# create is called when serializer.save() is invoked.
# It receives validated_data after all validation checks.
# We remove 'password2' (confirmation field) as it's not needed for user creation.
# User.objects.create_user() hashes the password and saves the user securely.
# The created user instance is returned and will be serialized in the response.
    def create(self, validated_data):
        role = validated_data.pop("role","client")
        validated_data.pop('password2')
        # validated_data.pop('password2') → removes the confirmation field (not needed for DB)
        user = User.objects.create_user(**validated_data)
          
        # Assign group automatically
        #  prevents crashes on fresh databases
        group, _ = Group.objects.get_or_create(name=role)
        group = Group.objects.get(name=role)
        user.groups.add(group)
        
        return user
    
        
class UserSerializer(serializers.ModelSerializer):
    # Exposes the group name (client/cleaner/admin) on read
    role = serializers.CharField( read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email','role']
        read_only_fields = ['id','role']

class AssignGroupSerializer(serializers.Serializer):
    group = serializers.ChoiceField(choices=["client", "cleaner"])

    def validate_group(self, value):
        if not Group.objects.filter(name=value).exists():
            raise serializers.ValidationError("Group does not exist.")
        return value