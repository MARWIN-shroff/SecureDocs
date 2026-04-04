from langgraph import StateGraph, END
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from django.conf import settings
from .rag_utils import create_embedding, chunk_text
from .models import Document

llm = OpenAI(api_key=settings.OPENAI_API_KEY)

# Define state
class AgentState:
    def __init__(self):
        self.document_content = ""
        self.metadata = {}
        self.chunks = []
        self.embeddings = []
        self.final_response = ""

# Define agents
def ingestion_agent(state: AgentState) -> AgentState:
    """Agent for document ingestion and initial processing."""
    # Read and preprocess document
    # This would be called with document content
    state.chunks = chunk_text(state.document_content)
    return state

def metadata_extraction_agent(state: AgentState) -> AgentState:
    """Agent for extracting metadata from document."""
    prompt = PromptTemplate(
        template="Extract metadata from the following document content:\n\n{content}\n\nExtract: title, author, date, summary",
        input_variables=["content"]
    )
    
    response_schemas = [
        ResponseSchema(name="title", description="Document title"),
        ResponseSchema(name="author", description="Document author"),
        ResponseSchema(name="date", description="Document date"),
        ResponseSchema(name="summary", description="Document summary")
    ]
    
    parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = parser.get_format_instructions()
    
    full_prompt = prompt.format(content=state.document_content) + "\n\n" + format_instructions
    
    response = llm(full_prompt)
    parsed = parser.parse(response)
    
    state.metadata = parsed
    return state

def embedding_agent(state: AgentState) -> AgentState:
    """Agent for creating embeddings."""
    state.embeddings = [create_embedding(chunk) for chunk in state.chunks]
    return state

def response_synthesis_agent(state: AgentState) -> AgentState:
    """Agent for synthesizing final response."""
    # This would be used for query responses
    # For now, placeholder
    state.final_response = "Document processed successfully"
    return state

# Build workflow
def create_document_processing_workflow():
    """Create LangGraph workflow for document processing."""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("ingestion", ingestion_agent)
    workflow.add_node("metadata", metadata_extraction_agent)
    workflow.add_node("embedding", embedding_agent)
    workflow.add_node("synthesis", response_synthesis_agent)
    
    # Add edges
    workflow.add_edge("ingestion", "metadata")
    workflow.add_edge("metadata", "embedding")
    workflow.add_edge("embedding", "synthesis")
    workflow.add_edge("synthesis", END)
    
    # Set entry point
    workflow.set_entry_point("ingestion")
    
    return workflow.compile()

# Usage
def process_document_with_agents(document_content: str) -> dict:
    """Process document using agent workflow."""
    workflow = create_document_processing_workflow()
    
    initial_state = AgentState()
    initial_state.document_content = document_content
    
    result = workflow.invoke(initial_state)
    
    return {
        'metadata': result.metadata,
        'chunks': result.chunks,
        'embeddings': result.embeddings,
        'response': result.final_response
    }