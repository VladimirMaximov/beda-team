export default function SelectedProducts({
    products,
    onRemove,
    onClear,
    onSearchRecipes,
    loading,
}) {
    return (
        <div className="card">
            <div className="block-header">
                <h2>Выбранные продукты</h2>

                {products.length > 0 && (
                    <button onClick={onClear} className="button-secondary">
                        Очистить
                    </button>
                )}
            </div>

            {products.length === 0 ? (
                <p className="empty-text">Пока нет выбранных продуктов</p>
            ) : (
                <div className="tags">
                    {products.map((product) => (
                        <div className="tag" key={product.id}>
                            <span>{product.name}</span>
                            <button
                                onClick={() => onRemove(product.id)}
                                className="tag-remove"
                            >
                                ×
                            </button>
                        </div>
                    ))}
                </div>
            )}

            <button
                onClick={onSearchRecipes}
                className="button-primary full-width"
                disabled={loading}
            >
                {loading ? "Поиск..." : "Подобрать рецепты"}
            </button>
        </div>
    );
}