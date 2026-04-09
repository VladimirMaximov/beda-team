# todo: delete module

from backend.models import Recipe

__all__ = [
    "build_recipe_match",
    "sort_recipe_matches",

]

def build_recipe_match(recipe: Recipe, user_ingredient_ids: set[int]) -> dict | None:
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