# CivicRAG - Civic & Tenant Rights AI Assistant

Developed as part of a Backend AI Engineering project-based internship at **FlyRank**. 
CivicRAG is a Retrieval-Augmented Generation (RAG) application built to solve a pressing society problem: **making complex civic laws and tenant rights accessible and understandable for everyday citizens.**

## 🌟 Project Highlights

- **AI-Powered RAG Architecture:** Integrates **Google Gemini** to deliver context-aware, highly accurate AI responses grounded strictly in ingested legal documents, preventing AI hallucinations.
- **Modular API Design:** Engineered a robust monolith with **FastAPI**, featuring 10+ RESTful API endpoints following strict Separation of Concerns.
- **Robust Storage:** Utilizes **PostgreSQL** with **pgvector** and custom connection pooling for lightning-fast relational document and semantic vector storage.
- **Containerized Deployment:** Fully containerized using **Docker** and `docker-compose` for streamlined environments.

## 🏗️ Core Backend Modules

The backend follows modular software architecture principles, broken down into 4 core pipelines:
1. **Document Management (`document_management`)**: Handles ingestion, text extraction, and chunking of civic documents.
2. **Retrieval Pipelines (`retrieval_pipelines`)**: Manages embeddings and semantic vector search to fetch the most relevant legal context.
3. **LLM Orchestration (`llm_orchestration`)**: Structures prompt engineering and manages asynchronous communication with the Google Gemini API.
4. **Conversation Workflows (`conversation_workflows`)**: Tracks session histories and manages the multi-turn chat lifecycle.

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Google Gemini API Key

### 1. Environment Setup
Create a `.env` file in the root directory and add your API key:
```env
GEMINI_API_KEY=your_google_gemini_key_here
```

### 2. Run with Docker
Spin up the entire RAG pipeline with a single command:
```bash
docker-compose up --build
```
The API will be available at `http://localhost:8000`.

### 3. API Documentation
Explore and test the 10+ endpoints dynamically via Swagger UI:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)

---
*Developed by the Backend AI Engineering Intern at FlyRank.*
