# IKARUS Furniture Recommender — FastAPI + React + Vector DB

End‑to‑end ML/NLP/CV/GenAI web app that recommends furniture, groups similar items, classifies product images, and generates creative copy.

## Quick Start (Dev)

### 1) Python backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r ../requirements.txt
# put dataset CSV at backend/app/data/intern_data_ikarus.csv
uvicorn app.main:app --reload --port 8000
```

### 2) React frontend
```bash
cd frontend
# if npm init vite wasn't run, this skeleton uses plain Vite config below
npm install
npm run dev  # runs on 5173
```

Open http://localhost:5173. The frontend calls FastAPI at http://localhost:8000.

## Env variables (optional)
- `PINECONE_API_KEY` and `PINECONE_INDEX` to use Pinecone instead of local FAISS.
- `EMBED_MODEL` (default: `sentence-transformers/all-MiniLM-L6-v2`)

## What’s included
- **Vector DB**: Pinecone (if key provided) or FAISS fallback, via LangChain.
- **ML**: Content-based recommendations from text + category embeddings.
- **NLP**: Clustering & similar-products grouping (UMAP + HDBSCAN/ KMeans).
- **CV**: Transfer-learning classifier stub (ResNet18) + prediction API.
- **GenAI**: Lightweight Transformers pipeline to generate product copy.
- **Analytics**: Notebook + API that aggregates pricing/brands/categories for charts.
- **React**: Two routes — `/` chat-like recommender, `/analytics` charts.
