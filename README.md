# SecureDocs

AI-powered document intelligence platform enabling secure storage, semantic search, and verification using LLM-driven retrieval pipelines.

## Features

- **Secure Document Storage**: Tamper-proof document storage with blockchain verification
- **Semantic Search**: RAG architecture with embedding models and FAISS vector databases
- **Agentic Workflows**: LangGraph-powered agents for ingestion, metadata extraction, and response synthesis
- **Blockchain Verification**: Ethereum-based hash verification for document authenticity
- **OTP Authentication**: Secure user authentication with TOTP

## Architecture

### Backend (Django REST API)
- Document upload and management
- RAG pipeline with LangChain and FAISS
- LangGraph agent workflows
- Blockchain integration with Web3.py
- JWT authentication with OTP

### Frontend (Angular)
- Document upload interface
- Search and verification UI
- User authentication

### Smart Contracts (Ethereum)
- Document hash registry on blockchain
- Tamper-proof verification

## Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
ng serve
```

### Smart Contracts Setup
```bash
cd smart-contracts
npm install
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost
```

## API Endpoints

- `POST /api/register/` - Register user with OTP
- `POST /api/verify-otp/` - Verify OTP for login
- `POST /api/upload/` - Upload document
- `POST /api/search/` - Semantic search
- `GET /api/documents/{id}/verify/` - Verify document on blockchain

## Technologies

- Django, DRF, LangChain, FAISS, LangGraph
- Angular, TypeScript
- Solidity, Hardhat, Web3.js
- OpenAI GPT, Sentence Transformers
