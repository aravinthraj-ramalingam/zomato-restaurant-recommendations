from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
try:
    from .schemas import RecommendationRequest, RecommendationResponse, OptionsResponse
    from .db_service import get_candidates, get_options
    from .ai_service import generate_recommendation_rationale
except ImportError:
    from api.schemas import RecommendationRequest, RecommendationResponse, OptionsResponse
    from api.db_service import get_candidates, get_options
    from api.ai_service import generate_recommendation_rationale
import uvicorn
from typing import Optional

app = FastAPI(title="Zomato AI Recommendation Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/options", response_model=OptionsResponse)
async def get_options_endpoint(location: Optional[str] = None):
    try:
        return get_options(location=location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recommend", response_model=RecommendationResponse)
async def get_recommendation(req: RecommendationRequest):
    try:
        candidates = get_candidates(
            place=req.place,
            cuisine=req.cuisine,
            max_price=req.max_price,
            min_rating=req.min_rating,
            limit=20
        )
        
        user_prefs = req.model_dump()
        rationale = generate_recommendation_rationale(user_prefs, candidates)
        
        return RecommendationResponse(
            recommendations=candidates,
            llm_rationale=rationale
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
