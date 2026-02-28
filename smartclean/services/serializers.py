from rest_framework import serializers
from .models import Service,JobService

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at']
        
        # remove null price orzero
        def validate_price(self,value):
            if value <=0:
                raise serializers.ValidationError("The base price must be greater than zero")
            return value
        
class JobServiceSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source = 'service.name',read_only= True)
    total_price = serializers.DecimalField( max_digits=8, decimal_places=2, read_only=True)
    
    class Meta:
        model = JobService
        fields = [  'id', 'job', 'service', 'service_name', 'quantity', 'unit_price', 'total_price']
        read_only_fields = ['id', 'unit_price', 'total_price']
    
    def create(self, validated_data):
        # Auto-snapshot the price from the service at time of booking
        service = validated_data['service']
        validated_data['unit_price'] = service.base_price
        return super().create(validated_data)

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value