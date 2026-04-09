import { apiFetch } from "./client";

export async function searchRecipes(ingredientIds) {
    return apiFetch("/api/recipes/search", {
        method: "POST",
        body: JSON.stringify({
            ingredient_ids: ingredientIds,
        }),
    });
}