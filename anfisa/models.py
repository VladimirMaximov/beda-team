from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Text

Base = declarative_base()


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    instructions = Column(Text)
    url = Column(String)
    source = Column(String)
    ingredients_text = Column(Text)

    # Необязательное поле: строка вида "1,5,10"
    # В нормальной схеме его можно потом убрать,
    # потому что связь и так хранится в таблице ingredients.
    ingredient_ids = Column(Text)

    ingredients = relationship(
        'Ingredient',
        back_populates='recipe',
        cascade='all, delete-orphan'
    )


class IngredientName(Base):
    __tablename__ = 'ingredient_names'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)

    ingredients = relationship(
        'Ingredient',
        back_populates='ingredient_name',
        cascade='all, delete-orphan'
    )


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredient_names.id"), nullable=False, index=True)
    quantity = Column(String, nullable=True)
    unit = Column(String, nullable=True)

    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient_name = relationship("IngredientName", back_populates="ingredients")