from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from roma.app.database import get_db
from roma.app.schemas import RecipeSearchRequest, RecipeSearchResponse
from roma.app.repositories.recipes import get_all_recipes_with_ingredients
from roma.app.matcher import build_recipe_match, sort_recipe_matches

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.post("/search", response_model=RecipeSearchResponse)
def search_recipes(
    payload: RecipeSearchRequest,
    db: Session = Depends(get_db),
):
    user_ingredient_ids = set(payload.ingredient_ids)

    if not user_ingredient_ids:
        raise HTTPException(status_code=400, detail="ingredient_ids must not be empty")

    recipes = get_all_recipes_with_ingredients(db)

    results = []
    for recipe in recipes:
        match_data = build_recipe_match(recipe, user_ingredient_ids)
        if match_data is None:
            continue

        # оставляем только рецепты, где есть хотя бы одно совпадение
        if len(match_data["matched_ingredients"]) > 0:
            results.append(match_data)

    sorted_results = sort_recipe_matches(results)[:10]

    return {"recipes": sorted_results}