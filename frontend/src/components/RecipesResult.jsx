export default function RecipesResult({ recipes }) {
    return (
        <div className="card">
            <h2>Результаты</h2>

            {recipes.length === 0 ? (
                <p className="empty-text">
                    Здесь позже можно сделать красивые карточки рецептов.
                </p>
            ) : (
                <div className="recipes-list">
                    {recipes.map((recipe) => (
                        <div className="recipe-card" key={recipe.id}>
                            <h3>{recipe.title}</h3>

                            <p className="recipe-score">
                                Совпадение: {recipe.score}
                            </p>

                            {recipe.matched_ingredients?.length > 0 && (
                                <div className="recipe-section">
                                    <strong>Совпавшие продукты:</strong>
                                    <div className="tags small-tags">
                                        {recipe.matched_ingredients.map((item) => (
                                            <div className="tag" key={item}>
                                                {item}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {recipe.missing_ingredients?.length > 0 && (
                                <div className="recipe-section">
                                    <strong>Недостающие продукты:</strong>
                                    <div className="tags small-tags">
                                        {recipe.missing_ingredients.map((item) => (
                                            <div className="tag tag-outline" key={item}>
                                                {item}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}