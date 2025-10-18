import os, typing as t
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Pinecone as LC_Pinecone
from pinecone import Pinecone
from pydantic import BaseModel

class VSConfig(BaseModel):
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    namespace: str = "ikarus-furniture"

def get_embedder(model_name: str):
    return HuggingFaceEmbeddings(model_name=model_name)

def build_or_load_vectorstore(texts: t.List[str], metadatas: t.List[dict], ids: t.List[str], cfg: VSConfig):
    use_pinecone = os.environ.get("PINECONE_API_KEY")
    emb = get_embedder(cfg.model_name)
    if use_pinecone:
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        index_name = os.environ.get("PINECONE_INDEX", "ikarus-furniture")
        if index_name not in [i["name"] for i in pc.list_indexes().indexes]:
            pc.create_index(name=index_name, dimension=384, metric="cosine")  # 384 for MiniLM-L6
        vectorstore = LC_Pinecone.from_texts(texts=texts, embedding=emb, metadatas=metadatas, index_name=index_name, namespace=cfg.namespace)
        return vectorstore
    # FAISS fallback (local)
    return FAISS.from_texts(texts=texts, embedding=emb, metadatas=metadatas)
