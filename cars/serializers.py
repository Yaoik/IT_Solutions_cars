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
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Car
        fields = ('id', 'make', 'model', 'year', 'description', 'owner')
        read_only_fields = ('id',)