from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.configurations.database import get_async_session
from backend.schemas import IngredientSearchResponse
from backend.services import search_ingredients

ingredients_router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@ingredients_router.get("/search", response_model=IngredientSearchResponse)
async def search_ingredients_endpoint(
    q: str = Query(..., min_length=1, description="Строка поиска ингредиента"),
    limit: int = Query(None, ge=1, le=100, description="Количество подсказок"),
    session: AsyncSession = Depends(get_async_session),
):
    items = await search_ingredients(session=session, query=q, limit=limit)
    return {"items": items}