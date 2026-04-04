from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    otp_secret = models.CharField(max_length=32, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    hash = models.CharField(max_length=64, unique=True)
    blockchain_tx = models.CharField(max_length=66, blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)

    def __str__(self):
        return self.title

class DocumentChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    content = models.TextField()
    embedding = models.JSONField()  # Store vector as list of floats
    chunk_index = models.IntegerField()

    class Meta:
        unique_together = ('document', 'chunk_index')

    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.document.title}"
