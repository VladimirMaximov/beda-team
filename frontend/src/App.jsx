import { useState } from "react";
import ProductSearch from "./components/ProductSearch";
import SelectedProducts from "./components/SelectedProducts";
import RecipesResult from "./components/RecipesResult";
import { searchRecipes } from "./api/recipes";

export default function App() {
    const [selectedProducts, setSelectedProducts] = useState([]);
    const [recipes, setRecipes] = useState([]);
    const [loadingRecipes, setLoadingRecipes] = useState(false);
    const [error, setError] = useState("");

    function addProduct(product) {
        const exists = selectedProducts.some((item) => item.id === product.id);
        if (exists) return;

        setSelectedProducts((prev) => [...prev, product]);
    }

    function removeProduct(productId) {
        setSelectedProducts((prev) =>
            prev.filter((item) => item.id !== productId)
        );
    }

    function clearProducts() {
        setSelectedProducts([]);
        setRecipes([]);
        setError("");
    }

    async function handleRecipeSearch() {
        if (selectedProducts.length === 0) {
            setError("Сначала добавьте хотя бы один продукт");
            setRecipes([]);
            return;
        }

        try {
            setLoadingRecipes(true);
            setError("");

            const ingredientIds = selectedProducts.map((item) => item.id);
            const data = await searchRecipes(ingredientIds);

            const recipeList = Array.isArray(data) ? data : data.recipes || [];
            setRecipes(recipeList);
        } catch (err) {
            setRecipes([]);
            setError(err.message || "Ошибка при поиске рецептов");
        } finally {
            setLoadingRecipes(false);
        }
    }

    return (
        <div className="page">
            <div className="container">
                <h1>Поиск рецептов по продуктам</h1>
                <p className="subtitle">
                    Выберите продукты, которые есть дома
                </p>

                <div className="layout">
                    <div className="left-column">
                        <ProductSearch
                            selectedProducts={selectedProducts}
                            onAddProduct={addProduct}
                        />

                        <SelectedProducts
                            products={selectedProducts}
                            onRemove={removeProduct}
                            onClear={clearProducts}
                            onSearchRecipes={handleRecipeSearch}
                            loading={loadingRecipes}
                        />

                        {error && <div className="error-box">{error}</div>}
                    </div>

                    <div className="right-column">
                        <RecipesResult recipes={recipes} />
                    </div>
                </div>
            </div>
        </div>
    );
}