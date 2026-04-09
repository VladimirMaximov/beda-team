from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from backend.models import IngredientName

__all__ = ["search_ingredients"]

async def search_ingredients(session: AsyncSession, query: str, limit: int = None) -> list[IngredientName]:
    if limit is None:
        limit = 20

    sql_query = (
        select(IngredientName)
        .where(func.lower(IngredientName.name).like(f"%{query.lower()}%"))
        .order_by(IngredientName.name.asc())
        .limit(limit)
    )
    result = await session.execute(sql_query)

    return result.scalars().all()