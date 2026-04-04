from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Document, User
from .serializers import DocumentSerializer, DocumentUploadSerializer, SearchQuerySerializer, UserSerializer
from .hashing import calculate_file_hash
from .blockchain import store_document_hash, verify_document_hash
from .rag_utils import process_document_for_rag, semantic_search, generate_response
from .langgraph_utils import process_document_with_agents
from .otp_utils import generate_otp_secret, verify_otp

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Document.objects.filter(uploaded_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_document(request):
    """Upload and process a document."""
    serializer = DocumentUploadSerializer(data=request.data)
    if serializer.is_valid():
        file_obj = serializer.validated_data['file']
        title = serializer.validated_data['title']
        
        # Calculate hash
        file_hash = calculate_file_hash(file_obj)
        
        # Check if document already exists
        if Document.objects.filter(hash=file_hash).exists():
            return Response({'error': 'Document already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create document
        document = Document.objects.create(
            title=title,
            file=file_obj,
            hash=file_hash,
            uploaded_by=request.user
        )
        
        # Process with LangGraph agents
        with open(document.file.path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        agent_result = process_document_with_agents(content)
        document.metadata = agent_result['metadata']
        document.save()
        
        # Process for RAG
        process_document_for_rag(document)
        
        # Store hash on blockchain
        try:
            tx_hash = store_document_hash(file_hash)
            document.blockchain_tx = tx_hash
            document.save()
        except Exception as e:
            # Log error but don't fail upload
            pass
        
        return Response(DocumentSerializer(document).data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_documents(request):
    """Semantic search through documents."""
    serializer = SearchQuerySerializer(data=request.data)
    if serializer.is_valid():
        query = serializer.validated_data['query']
        
        # Perform semantic search
        results = semantic_search(query)
        
        # Generate AI response
        response = generate_response(query)
        
        return Response({
            'results': results,
            'ai_response': response
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_user(request):
    """Register a new user with OTP setup."""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    phone = request.data.get('phone')
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, email=email, password=password, phone=phone)
    user.otp_secret = generate_otp_secret()
    user.save()
    
    return Response({
        'user': UserSerializer(user).data,
        'otp_secret': user.otp_secret  # In production, return QR code URI
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def verify_otp_login(request):
    """Verify OTP for login."""
    username = request.data.get('username')
    otp_token = request.data.get('otp_token')
    
    try:
        user = User.objects.get(username=username)
        if verify_otp(user.otp_secret, otp_token):
            # Generate JWT token here
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_document(request, document_id):
    """Verify document authenticity on blockchain."""
    document = get_object_or_404(Document, id=document_id, uploaded_by=request.user)
    
    try:
        is_valid = verify_document_hash(document.hash)
        return Response({'is_valid': is_valid})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
