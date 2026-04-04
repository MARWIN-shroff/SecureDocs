import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS as LangFAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.docstore.document import Document as LangDocument
from django.conf import settings
from .models import DocumentChunk

# Initialize models
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
llm = OpenAI(api_key=settings.OPENAI_API_KEY)

def create_embedding(text: str) -> np.ndarray:
    """Create embedding for text."""
    return embedding_model.encode(text)

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list:
    """Split text into chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks

def process_document_for_rag(document):
    """Process uploaded document for RAG."""
    # Read file content (assuming text files for now)
    with open(document.file.path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Chunk the content
    chunks = chunk_text(content)
    
    # Create embeddings and save chunks
    for i, chunk in enumerate(chunks):
        embedding = create_embedding(chunk)
        DocumentChunk.objects.create(
            document=document,
            content=chunk,
            embedding=embedding.tolist(),
            chunk_index=i
        )

def build_faiss_index():
    """Build FAISS index from all document chunks."""
    chunks = DocumentChunk.objects.all()
    if not chunks:
        return None
    
    embeddings = np.array([chunk.embedding for chunk in chunks])
    dimension = embeddings.shape[1]
    
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    # Store documents for retrieval
    documents = [LangDocument(page_content=chunk.content, metadata={'document_id': chunk.document.id}) 
                 for chunk in chunks]
    
    return LangFAISS.from_documents(documents, SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2'))

def semantic_search(query: str, top_k: int = 5):
    """Perform semantic search."""
    index = build_faiss_index()
    if not index:
        return []
    
    docs = index.similarity_search(query, k=top_k)
    return [{'content': doc.page_content, 'document_id': doc.metadata['document_id']} for doc in docs]

def generate_response(query: str) -> str:
    """Generate response using RAG."""
    index = build_faiss_index()
    if not index:
        return "No documents available for search."
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=index.as_retriever()
    )
    
    return qa_chain.run(query)