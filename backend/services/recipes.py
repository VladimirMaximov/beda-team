from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models import Recipe, Ingredient

__all__ = [
    "get_all_recipes_with_ingredients",
    "get_most_relevant_recipes",
    "get_recipes_by_ids",
    "score_recipe"
]

# todo: delete
async def get_all_recipes_with_ingredients(session: AsyncSession) -> list[Recipe]:
    # todo: rewrite

    query = (
        select(Recipe)
        .options(
            joinedload(Recipe.ingredients)
            .joinedload(Ingredient.ingredient_name)
        )
    )

    result = await session.execute(query)
    return result.scalars().all()

    # return (
    #     db.query(Recipe)
    #     .options(
    #         joinedload(Recipe.ingredients).joinedload(Ingredient.ingredient_name)
    #     )
    #     .all()
    # )

def sort_recipe_matches(matches: list[dict]) -> list[dict]:
    return sorted(
        matches,
        key=lambda item: (
            item["score"],
            len(item["matched_ingredients"]),
            -len(item["missing_ingredients"]),
        ),
        reverse=True,
    )

async def get_most_relevant_recipes(
        session: AsyncSession, user_ingredient_ids: set, limit: int = None
) -> list[int]:
    if limit is None:
        limit = 10

    recipe_ingredients = func.count(Ingredient.recipe_id)
    query = (
        select(Ingredient.recipe_id)
        .filter(Ingredient.ingredient_id.in_(user_ingredient_ids))
        .group_by(Ingredient.recipe_id)
        .order_by(recipe_ingredients.desc())
        .limit(limit)
    )
    result = await session.execute(query)

    return result.scalars().all()

async def get_recipes_by_ids(session: AsyncSession, recipe_ids: list[int]) -> list[Recipe]:
    query = (
        select(Recipe)
        .filter(Recipe.id.in_(recipe_ids))
        .options(
            selectinload(Recipe.ingredients).selectinload(Ingredient.ingredient_name)
        )
    )
    result = await session.execute(query)

    return result.scalars().all()

def score_recipe(recipe: Recipe, user_ingredient_ids) -> dict | None:
    recipe_ingredients = recipe.ingredients or []

    recipe_ing_ids = {
        item.ingredient_id
        for item in recipe_ingredients
        if item.ingredient_id is not None
    }

    if not recipe_ing_ids:
        return None

    matched_ids = recipe_ing_ids & user_ingredient_ids
    missing_ids = recipe_ing_ids - user_ingredient_ids

    matched_names = []
    missing_names = []

    for item in recipe_ingredients:
        if item.ingredient_name is None:
            continue

        ing_name = item.ingredient_name.name

        if item.ingredient_id in matched_ids:
            matched_names.append(ing_name)
        elif item.ingredient_id in missing_ids:
            missing_names.append(ing_name)

    score = len(matched_ids) / len(recipe_ing_ids)

    return {
        "id": recipe.id,
        "title": recipe.title,
        "url": recipe.url,
        "score": round(score, 4),
        "matched_ingredients": sorted(set(matched_names)),
        "missing_ingredients": sorted(set(missing_names)),
    }

