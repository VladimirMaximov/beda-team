from sqlalchemy.orm import Session, joinedload

from anfisa.models import Recipe, Ingredient


def get_all_recipes_with_ingredients(db: Session) -> list[Recipe]:
    return (
        db.query(Recipe)
        .options(
            joinedload(Recipe.ingredients).joinedload(Ingredient.ingredient_name)
        )
        .all()
    )