from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from PIL import Image
import io

from .recommend import RecommendRequest, RecommendResponse, recommend
from .genai import generate_copy
from .analytics import summary
from .cv_model import predict_image_category

app = FastAPI(title="IKARUS Furniture Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CopyRequest(BaseModel):
    title: str
    brand: str = ""
    material: str = ""
    color: str = ""
    categories: str = ""
    user_prompt: str = ""

@app.post("/api/recommend", response_model=RecommendResponse)
def api_recommend(payload: RecommendRequest):
    items = recommend(payload.query, payload.top_k)
    # attach generated copy
    for it in items:
        it["gen_copy"] = generate_copy(it.get("title",""), it.get("brand",""), it.get("material",""), it.get("color",""), it.get("categories",""), payload.query)
    return {"items": items}

@app.post("/api/generate-copy")
def api_generate_copy(payload: CopyRequest):
    text = generate_copy(payload.title, payload.brand, payload.material, payload.color, payload.categories, payload.user_prompt)
    return {"copy": text}

@app.get("/api/analytics")
def api_analytics():
    return summary()

@app.post("/api/cv/predict")
async def api_cv_predict(file: UploadFile = File(...)):
    content = await file.read()
    img = Image.open(io.BytesIO(content)).convert("RGB")
    label = predict_image_category(img)
    return {"prediction": label}
