from rest_framework import serializers
from .models import Job
from services.models import Service


class JobSerializer(serializers.ModelSerializer):
    services = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        many=True
    )

    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ["client", "status", "total_price"]