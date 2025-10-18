import pandas as pd, numpy as np, typing as t
from pydantic import BaseModel
from .vectorstore import build_or_load_vectorstore, VSConfig
from .utils import load_dataset

class RecommendRequest(BaseModel):
    query: str
    top_k: int = 5

class RecommendResponse(BaseModel):
    items: t.List[dict]

# Build vector store at import time (for dev; for prod, move to startup event)
_df = load_dataset()
_texts = (_df["title"].fillna('') + " " + _df["description"].fillna('') + " categories: " + _df["categories"].fillna('')).tolist()
_metas = _df.fillna("").to_dict(orient="records")
_ids = [str(x) for x in _df.get("uniq_id", _df.index.astype(str))]

_vectorstore = build_or_load_vectorstore(_texts, _metas, _ids, VSConfig())

def recommend(query: str, top_k: int = 5) -> t.List[dict]:
    docs = _vectorstore.similarity_search(query, k=top_k)
    out = []
    for d in docs:
        meta = dict(d.metadata)
        meta["score_hint"] = getattr(d, "score", None)
        out.append(meta)
    return out
