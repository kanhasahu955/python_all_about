# Resume Analyzer

Agentic resume analysis with RAG: **FastAPI**, **LangChain**, **LangGraph**, **MySQL**, **Pinecone**, and **Nuxt 3**.

## Architecture

| Layer | Role |
|--------|------|
| **Nuxt 3** | Upload resume, job description UI, chat with the analyzer, show scores and citations |
| **FastAPI** | REST + WebSocket; orchestrates agents, RAG, and persistence |
| **LangGraph** | Multi-step agent: parse → retrieve similar chunks → score vs JD → optional rewrite suggestions |
| **RAG** | Chunk resume text → embeddings → Pinecone; retrieve top-k for grounded answers |
| **MySQL** | Users, sessions, resume metadata, analysis history, optional raw text pointers |
| **Pinecone** | Vector index per user or per resume (namespace) for semantic search |

## Flow (high level)

1. User uploads PDF/text; backend extracts text, stores metadata in MySQL, chunks and upserts vectors to Pinecone.
2. User provides a job description (or selects a saved one).
3. LangGraph agent nodes: retrieve relevant resume chunks → LLM compares to JD → structured output (fit score, gaps, strengths).
4. Responses cite chunk IDs or snippets from retrieved context (grounded RAG).

## Prerequisites

- Python 3.11+
- Node 20+
- MySQL 8+
- Pinecone account + index (dimension must match your embedding model, e.g. 1536 for `text-embedding-3-small`)
- OpenAI or another provider supported by LangChain for embeddings + chat

## Quick start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with MYSQL_*, PINECONE_*, OPENAI_API_KEY
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
# Set NUXT_PUBLIC_API_BASE=http://localhost:8000
npm run dev
```

## Project layout

```
resume-analyzer/
├── backend/app/
│   ├── main.py           # FastAPI app
│   ├── config.py         # Settings
│   ├── api/              # Routes
│   ├── rag/              # Embeddings, Pinecone, chunking
│   ├── agents/           # LangGraph graph + nodes
│   └── db/               # MySQL SQLAlchemy models
└── frontend/             # Nuxt 3
```

## Security notes

- Never commit `.env`. Use server-side only keys for Pinecone and DB; scope Pinecone namespaces by user ID.
- Validate file types and size on upload; scan PDFs safely in production.
