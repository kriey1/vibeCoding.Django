from rest_framework import serializers
from .models import Post, Comment, FileUpload


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']


class FileUploadSerializer(serializers.ModelSerializer):
    uploader = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = FileUpload
        fields = ['id', 'post', 'uploader', 'file', 'filename', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    files = FileUploadSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'comments', 'files']
