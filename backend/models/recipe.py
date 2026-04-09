from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text

from .base import BaseModel

__all__ = ["Recipe"]

class Recipe(BaseModel):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    instructions = Column(Text)
    url = Column(String)
    source = Column(String)
    ingredients_text = Column(Text)

    ingredient_ids = Column(Text, nullable=True)

    ingredients = relationship(
        'Ingredient',
        back_populates='recipe',
        cascade='all, delete-orphan'
    )