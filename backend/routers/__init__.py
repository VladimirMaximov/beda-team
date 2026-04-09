from fastapi import APIRouter

from .ingredients import ingredients_router
from .recipes import recipes_router

router = APIRouter(prefix="/api", tags=["api"])

router.include_router(ingredients_router)
router.include_router(recipes_router)