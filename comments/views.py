from django.shortcuts import render
from rest_framework import viewsets, permissions
from .permissons import IsCommentOwnerAndCreateOrReadOnly, IsAuthenticatedOrReadOnly
from .serializers import CommentSerializer
from .models import Comment


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для Comment !только CREATE и READ!"""
    throttle_scope = 'comment'
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentOwnerAndCreateOrReadOnly]

    def get_queryset(self):
        car_id = self.kwargs['car_id']
        return Comment.objects.filter(car_id=car_id)
    
    def perform_create(self, serializer):
        car_id = self.kwargs['car_id']
        serializer.context['car_id'] = car_id
        serializer.save(author=self.request.user)