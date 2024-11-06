from django.shortcuts import render
from rest_framework import viewsets, permissions
from .permissons import IsCommentOwnerAndCreateOrReadOnly, IsAuthenticatedOrReadOnly
from .serializers import CommentSerializer
from .models import Comment



class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для Comment !только POST!"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentOwnerAndCreateOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, car=self.kwargs['car_id'])