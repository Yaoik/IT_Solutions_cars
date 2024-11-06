from rest_framework import serializers
from rest_framework import serializers
from users.models import User
from .models import Comment, Car
from django.conf import settings
import logging


logger = logging.getLogger(__name__)

class CommentSerializer(serializers.ModelSerializer):
    """Serializer для добавления и обновления Comment"""
    
    author = serializers.ReadOnlyField(source='author.username')
    car = serializers.ReadOnlyField(source='car.id')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'car', 'created_at')
        read_only_fields = ('id', 'created_at', 'car', 'user' )
        
    def create(self, validated_data):
        validated_data['car'] = Car.objects.get(id=self.context['car_id'])
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)   
    
    def to_representation(self, instance:Comment):
        representation = super().to_representation(instance)
        return representation