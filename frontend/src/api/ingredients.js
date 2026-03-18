import { apiFetch } from "./client";

export async function searchIngredients(query) {
    return apiFetch(
        `/ingredients/search?q=${encodeURIComponent(query)}&limit=5`
    );
}