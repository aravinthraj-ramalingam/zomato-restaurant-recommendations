from pydantic import BaseModel, Field
from typing import Optional, List

class RecommendationRequest(BaseModel):
    place: str = Field(..., description="Location/City to search for restaurants")
    cuisine: str = Field(..., description="Desired cuisine (e.g., North Indian, Chinese)")
    max_price: Optional[float] = Field(None, description="Maximum cost for two people")
    min_rating: Optional[float] = Field(None, description="Minimum allowed rating out of 5")

class RestaurantCandidate(BaseModel):
    name: str
    address: str
    rate: Optional[float]
    cost: Optional[float]
    cuisines: str
    url: str

class RecommendationResponse(BaseModel):
    recommendations: List[dict]
    llm_rationale: str

class OptionsResponse(BaseModel):
    locations: List[str]
    cuisines: List[str]
