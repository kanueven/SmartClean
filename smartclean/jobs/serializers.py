from rest_framework import serializers
from .models import Job
from services.models import Service


class JobSerializer(serializers.ModelSerializer):
    services = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        many=True,
        required = False
    )
    # Show service names alongside ids
    service_names = serializers.SerializerMethodField()
    # Show client username in responses
    client_username = serializers.CharField(source='client.user.username', read_only=True)
    # Show cleaner username in responses
    cleaner_username = serializers.CharField(source='cleaner.user.username', read_only=True, allow_null=True)

    class Meta:
        model = Job
        fields = "__all__"
        # client and status are set by the system, not the user
        read_only_fields = ['client', 'status', 'quoted_price', 'quote_approved_at',
                            'started_at', 'completed_at', 'created_at', 'updated_at']

    def get_service_names(self, obj):
        return [service.name for service in obj.services.all()]
    def validate_client_rating(self, value):
        if value is not None and not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value