from typing import List

from pydantic import BaseModel

__all__ = [
    "IngredientItem",
    "IngredientSearchResponse"
]

class IngredientItem(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class IngredientSearchResponse(BaseModel):
    items: List[IngredientItem]