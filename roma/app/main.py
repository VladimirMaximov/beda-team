from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from roma.app.routers.ingredients import router as ingredients_router
from roma.app.routers.recipes import router as recipes_router

app = FastAPI(title="Recipe Matcher API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # потом лучше заменить на адрес frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingredients_router)
app.include_router(recipes_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Recipe API is running"}