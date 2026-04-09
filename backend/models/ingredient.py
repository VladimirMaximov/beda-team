from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from .base import BaseModel

__all__ = ["Ingredient"]

class Ingredient(BaseModel):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)  # todo: удалить
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredient_names.id"), nullable=False, index=True)
    quantity = Column(String, nullable=True)
    unit = Column(String, nullable=True)

    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient_name = relationship("IngredientName", back_populates="ingredients")