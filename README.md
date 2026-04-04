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

### Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
ng serve
```

### Smart Contracts
```bash
cd smart-contracts
npm install
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost
```

## Usage

1. Register user with OTP setup
2. Upload documents (processed by AI agents)
3. Search documents semantically
4. Verify document authenticity on blockchain

## Technologies

- Django, DRF, LangChain, FAISS, LangGraph
- Angular, TypeScript
- Solidity, Hardhat, Web3.js
- OpenAI GPT, Sentence Transformers
