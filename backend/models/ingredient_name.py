from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

from .base import BaseModel

__all__ = ["IngredientName"]

class IngredientName(BaseModel):
    __tablename__ = 'ingredient_names'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)

    ingredients = relationship(
        'Ingredient',
        back_populates='ingredient_name',
        cascade='all, delete-orphan'
    )