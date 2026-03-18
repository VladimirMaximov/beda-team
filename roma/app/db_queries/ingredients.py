from sqlalchemy.orm import Session
from sqlalchemy import func

from anfisa.models import IngredientName


def search_ingredients(db: Session, query: str, limit: int = None) -> list[IngredientName]:
    if limit is None:
        limit = 5
    return (
        db.query(IngredientName)
        .filter(func.lower(IngredientName.name).like(f"%{query.lower()}%"))
        .order_by(IngredientName.name.asc())
        .limit(limit)
        .all()
    )