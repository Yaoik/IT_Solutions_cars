from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import User
from .models import Car, Make
import logging


logger = logging.getLogger(__name__)

class CarSerializer(serializers.ModelSerializer):
    make = serializers.CharField()
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Car
        fields = ('id', 'make', 'model', 'year', 'description', 'owner')
        read_only_fields = ('id',)
        
    def validate_make(self, value):
        if value is None or value == '':
            raise serializers.ValidationError('Поле Make обязательно!')
        make, created = Make.objects.get_or_create(name=value)
        return make
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)   
    
    def to_representation(self, instance:Car):
        representation = super().to_representation(instance)
        representation['make'] = instance.make.name # type: ignore
        return representation