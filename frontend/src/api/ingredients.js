import { apiFetch } from "./client";

export async function searchIngredients(query) {
    return apiFetch(
        `/api/ingredients/search?q=${encodeURIComponent(query)}&limit=5`
    );
}