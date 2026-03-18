from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from roma.app.database import get_db
from roma.app.schemas import IngredientSearchResponse
from roma.app.repositories.ingredients import search_ingredients

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.get("/search", response_model=IngredientSearchResponse)
def search_ingredients_endpoint(
    q: str = Query(..., min_length=1, description="Строка поиска ингредиента"),
    limit: int = Query(None, ge=1, le=100, description="Количество подсказок"),
    db: Session = Depends(get_db),
):
    items = search_ingredients(db=db, query=q, limit=limit)
    return {"items": items}