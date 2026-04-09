from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from icecream import ic  #  todo: delete

from backend.configurations.database import get_async_session
from backend.schemas import RecipeSearchRequest, RecipeSearchResponse
from backend.services import (get_all_recipes_with_ingredients, build_recipe_match,
                              sort_recipe_matches, get_most_relevant_recipes, get_recipes_by_ids, score_recipe)
recipes_router = APIRouter(prefix="/recipes", tags=["recipes"])

@recipes_router.post("/search", response_model=RecipeSearchResponse)
async def search_recipes(
    payload: RecipeSearchRequest,
    session: AsyncSession = Depends(get_async_session),
):
    user_ingredient_ids = set(payload.ingredient_ids)

    if not user_ingredient_ids:
        raise HTTPException(status_code=400, detail="ingredient_ids must not be empty")


    # todo: add function from services.recipes
    recipe_ids = await get_most_relevant_recipes(session, user_ingredient_ids)
    ic("look here")  # todo: delete
    ic(recipe_ids)

    recipes = await get_recipes_by_ids(session, recipe_ids)
    ic(recipes)
    ic(type(recipes))  # todo: delete

    result = []
    for recipe in recipes:
        result.append(score_recipe(recipe, user_ingredient_ids))

    return {"recipes": result}

    # recipes = await get_all_recipes_with_ingredients(session)  # todo: useless
    #
    # # todo: may be replaced with select query
    # results = []
    # for recipe in recipes:
    #     match_data = build_recipe_match(recipe, user_ingredient_ids)
    #     if match_data is None:
    #         continue
    #
    #     # оставляем только рецепты, где есть хотя бы одно совпадение
    #     if len(match_data["matched_ingredients"]) > 0:
    #         results.append(match_data)
    #
    # sorted_results = sort_recipe_matches(results)[:10]
    #
    # return {"recipes": sorted_results}