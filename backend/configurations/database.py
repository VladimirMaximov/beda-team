from typing import AsyncGenerator, Callable, Optional

from icecream import ic  # todo: delete
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from backend.models.base import BaseModel
from backend.models import *
from .settings import settings
from .db_creator import *

__async_engine: AsyncEngine | None = None
__session_factory: Optional[Callable[[], AsyncSession]] = None

SQLALCHEMY_DATABASE_URL = settings.database_url


def global_init() -> None:
    global __async_engine, __session_factory

    if __session_factory:
        return

    if not __async_engine:
        __async_engine = create_async_engine(url=SQLALCHEMY_DATABASE_URL, echo=False)

    __session_factory = async_sessionmaker(__async_engine)


async def get_async_session() -> AsyncGenerator:
    global __session_factory

    if not __session_factory:
        raise ValueError({"message": "You must call global_init() before using this method"})

    session: AsyncSession = __session_factory()

    try:
        yield session
        await session.commit()
    except Exception as e:
        raise e
    finally:
        await session.rollback()
        await session.close()


async def create_db_and_tables():
    global __session_factory
    global __async_engine

    if __async_engine is None:
        raise ValueError({"message": "You must call global_init() before using this method."})

    async with __async_engine.begin() as conn:
        # await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

    # getting session and checking non-emptiness of DB tables
    async with __session_factory() as session:
        ingredients_count = await session.scalar(select(func.count()).select_from(Ingredient))
        ingredient_names_count = await session.scalar(select(func.count()).select_from(IngredientName))
        recipes_count = await session.scalar(select(func.count()).select_from(Recipe))

    if ingredients_count < 100 or ingredient_names_count < 10 or recipes_count < 10:
        async with __async_engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)
            await conn.run_sync(BaseModel.metadata.create_all)

        async with __session_factory() as session:
            validate_files()

            recipes_df, ingredients_df = load_dataframes()

            name_to_id = await fill_ingredient_names(session, ingredients_df)
            await fill_recipes(session, recipes_df)
            recipe_to_ingredient_ids = await fill_recipe_ingredients(session, ingredients_df, name_to_id)
            await fill_recipe_ingredient_ids_field(session, recipe_to_ingredient_ids)


