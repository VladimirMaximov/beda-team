const API_BASE_URL = "http://localhost:8000";

export async function apiFetch(path, options = {}) {
    const response = await fetch(`${API_BASE_URL}${path}`, {
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        },
        ...options,
    });

    if (!response.ok) {
        let errorMessage = "Ошибка запроса к серверу";

        try {
            const errorData = await response.json();
            errorMessage =
                errorData.detail ||
                errorData.error ||
                errorData.message ||
                errorMessage;
        } catch {
            // оставляем стандартное сообщение
        }

        throw new Error(errorMessage);
    }

    return response.json();
}