# beda-team

# 🍳 Recipe Finder (beda-team)

Веб-приложение для подбора рецептов на основе имеющихся ингредиентов.

Проект представляет собой fullstack-систему, включающую:
- парсинг рецептов
- хранение данных в базе
- backend API
- frontend интерфейс

---

## 🚀 Возможности

- 🔍 Поиск ингредиентов (autocomplete)
- 🥕 Выбор доступных продуктов
- 🍝 Подбор рецептов по ингредиентам
- 🔗 Отображение ссылок на оригинальные рецепты
- ⚡ Быстрая работа через REST API

---

## 🧩 Архитектура проекта

project/
│
├── backend/        # FastAPI сервер
├── frontend/       # React приложение
├── database/       # БД
├── parser/         # парсинг рецептов

---

## 🧠 Как работает система

1. Пользователь вводит ингредиенты
2. Frontend отправляет запрос на backend
3. Backend ищет рецепты
4. Возвращает список
5. Frontend отображает результат

---

## 🗄️ База данных

Таблицы:
- recipes
- ingredients
- recipe_ingredients

Связь many-to-many

---

## ⚙️ Backend (FastAPI)

### Эндпоинты:

GET /ingredients/search?q=tomato&limit=5  
GET /recipes/search?ingredient_ids=1,2,3  

---

## 🎨 Frontend (React)

- поиск ингредиентов
- выбор продуктов
- отображение рецептов

---

## 🕷️ Парсинг

Собирает:
- название
- ингредиенты
- ссылку

---

## 🔎 Алгоритм

- поиск совпадений
- сортировка по релевантности

---

## ▶️ Запуск

### Backend
cd backend  
pip install -r requirements.txt  
uvicorn main:app --reload  

### Frontend
cd frontend  
npm install  
npm run dev  

---

## 📈 Перспективы

- ML-рекомендации
- аккаунты
- избранное

---

## 📌 Итог

MVP веб-приложение для подбора рецептов с архитектурой:
парсинг → БД → API → frontend
