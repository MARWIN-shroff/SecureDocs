from rest_framework import serializers
from .models import Document, DocumentChunk, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone']

class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'hash', 'blockchain_tx', 'uploaded_by', 'uploaded_at', 'metadata']
        read_only_fields = ['hash', 'blockchain_tx', 'uploaded_by', 'uploaded_at']

class DocumentChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentChunk
        fields = ['id', 'document', 'content', 'chunk_index']

class DocumentUploadSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    file = serializers.FileField()

class SearchQuerySerializer(serializers.Serializer):
    query = serializers.CharField(max_length=500)
