from typing import List
from pydantic import BaseModel, Field


class IngredientItem(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class IngredientSearchResponse(BaseModel):
    items: List[IngredientItem]


class RecipeSearchRequest(BaseModel):
    ingredient_ids: List[int] = Field(..., min_length=1)


class RecipeItem(BaseModel):
    id: int
    title: str
    score: float
    matched_ingredients: List[str]
    missing_ingredients: List[str]


class RecipeSearchResponse(BaseModel):
    recipes: List[RecipeItem]