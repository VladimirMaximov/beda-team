from typing import List

from pydantic import BaseModel, Field

__all__ = [
    "RecipeItem",
    "RecipeSearchResponse",
    "RecipeSearchRequest"
]

class RecipeSearchRequest(BaseModel):
    ingredient_ids: List[int] = Field(..., min_length=1)


class RecipeItem(BaseModel):
    id: int
    title: str
    url: str
    score: float
    matched_ingredients: List[str]
    missing_ingredients: List[str]


class RecipeSearchResponse(BaseModel):
    recipes: List[RecipeItem]