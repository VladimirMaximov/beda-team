import { useEffect, useRef, useState } from "react";
import { searchIngredients } from "../api/ingredients";

export default function ProductSearch({ selectedProducts, onAddProduct }) {
    const [query, setQuery] = useState("");
    const [suggestions, setSuggestions] = useState([]);
    const [loading, setLoading] = useState(false);
    const [open, setOpen] = useState(false);
    const [error, setError] = useState("");

    const debounceRef = useRef(null);
    const wrapperRef = useRef(null);

    useEffect(() => {
        function handleClickOutside(event) {
            if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
                setOpen(false);
            }
        }

        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    useEffect(() => {
        if (debounceRef.current) {
            clearTimeout(debounceRef.current);
        }

        const trimmed = query.trim();

        if (!trimmed) {
            setSuggestions([]);
            setError("");
            return;
        }

        debounceRef.current = setTimeout(async () => {
            try {
                setLoading(true);
                setError("");

                const data = await searchIngredients(trimmed);
                const items = Array.isArray(data?.items) ? data.items : [];

                const normalized = items
                    .filter((item) => item && item.id != null && item.name)
                    .filter(
                        (item) =>
                            !selectedProducts.some((selected) => selected.id === item.id)
                    )
                    .slice(0, 5);

                setSuggestions(normalized);
                setOpen(true);
            } catch (err) {
                setSuggestions([]);
                setError(err.message || "Не удалось загрузить продукты");
            } finally {
                setLoading(false);
            }
        }, 300);

        return () => {
            if (debounceRef.current) {
                clearTimeout(debounceRef.current);
            }
        };
    }, [query, selectedProducts]);

    function handleAddOne(product) {
        onAddProduct(product);
        setQuery("");
        setSuggestions([]);
        setOpen(false);
        setError("");
    }

    function handleAddAll() {
        if (suggestions.length === 0) return;

        suggestions.forEach((item) => {
            onAddProduct(item);
        });

        setQuery("");
        setSuggestions([]);
        setOpen(false);
        setError("");
    }

    function handleKeyDown(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            handleAddAll();
        }
    }

    return (
        <div className="card" ref={wrapperRef}>
            <h2>Поиск продуктов</h2>

            <div className="search-row">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => {
                        setQuery(e.target.value);
                        setOpen(true);
                    }}
                    onKeyDown={handleKeyDown}
                    placeholder="Например: курица, картофель, сыр"
                    className="search-input"
                />

                <button onClick={handleAddAll} className="button-primary">
                    Добавить
                </button>
            </div>

            {error && <div className="error-box">{error}</div>}

            {open && (query.trim() || loading || suggestions.length > 0) && (
                <div className="suggestions-box">
                    {loading ? (
                        <div className="hint-text">Загрузка...</div>
                    ) : suggestions.length > 0 ? (
                        suggestions.map((item) => (
                            <button
                                key={item.id}
                                className="suggestion-item"
                                onClick={() => handleAddOne(item)}
                            >
                                {item.name}
                            </button>
                        ))
                    ) : (
                        <div className="hint-text">Подходящих вариантов нет</div>
                    )}
                </div>
            )}
        </div>
    );
}