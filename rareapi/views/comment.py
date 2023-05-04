from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Comment, RareUser, Post

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content','created_on')

class CommentView(ViewSet):
    def list(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    def create(self, request):
        comment = Comment()
        author = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=request.data['post'])
        content = request.data['content']
        created_on = request.data['created_on']
        comment.save()
        serialized = CommentSerializer(comment)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    def update(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        author = RareUser.objects.get(user=request.auth.user)
        comment.author = author
        post = Post.objects.get(pk=request.data['post'])
        comment.post = post
        comment.content = request.data['content']
        comment.created_on = request.data['created_on']
        comment.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, pk=None):
        comment=Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)