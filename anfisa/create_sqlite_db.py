from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from collections import defaultdict

from models import Base, Recipe, IngredientName, Ingredient


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'anton'
DB_PATH = BASE_DIR / 'recipes.db'

RECIPES_CSV = DATA_DIR / 'recipes_3_clean.csv'
RECIPE_INGREDIENTS_CSV = DATA_DIR / 'recipe_ingredients_3_clean.csv'


def create_engine_and_session():
    engine = create_engine(f'sqlite:///{DB_PATH}')
    SessionLocal = sessionmaker(bind=engine)
    return engine, SessionLocal


def validate_files() -> None:
    missing = []
    if not RECIPES_CSV.exists():
        missing.append(str(RECIPES_CSV))
    if not RECIPE_INGREDIENTS_CSV.exists():
        missing.append(str(RECIPE_INGREDIENTS_CSV))

    if missing:
        raise FileNotFoundError(
            'Не найдены CSV-файлы:\n' + '\n'.join(missing)
        )


def recreate_database(engine) -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    Base.metadata.create_all(engine)


def load_dataframes() -> tuple[pd.DataFrame, pd.DataFrame]:
    recipes_df = pd.read_csv(RECIPES_CSV)
    ingredients_df = pd.read_csv(RECIPE_INGREDIENTS_CSV)
    return recipes_df, ingredients_df


def fill_ingredient_names(session, ingredients_df: pd.DataFrame) -> dict[str, int]:
    unique_names = ingredients_df['ingredient'].dropna().unique()
    name_to_id: dict[str, int] = {}

    for name in unique_names:
        ing = IngredientName(name=str(name).strip())
        session.add(ing)
        session.flush()
        name_to_id[str(name).strip()] = ing.id

    session.commit()
    return name_to_id


def fill_recipes(session, recipes_df: pd.DataFrame) -> None:
    for _, row in recipes_df.iterrows():
        recipe = Recipe(
            id=int(row['id']),
            title=row['title'],
            instructions=row.get('instructions'),
            url=row.get('url'),
            source=row.get('source'),
            ingredients_text=row.get('ingredients_text')
        )
        session.add(recipe)

    session.commit()


def fill_recipe_ingredients(session, ingredients_df: pd.DataFrame, name_to_id: dict[str, int]) -> dict[int, list[int]]:
    recipe_to_ingredient_ids: dict[int, list[int]] = defaultdict(list)

    for _, row in ingredients_df.iterrows():
        ing_name = str(row['ingredient']).strip() if pd.notna(row['ingredient']) else None
        if not ing_name:
            continue

        ing_id = name_to_id.get(ing_name)
        if ing_id is None:
            continue

        raw_quantity = row.get("quantity")
        quantity = str(raw_quantity).strip() if pd.notna(raw_quantity) else None
        if quantity == "":
            quantity = None

        raw_unit = row.get("unit")
        unit = str(raw_unit).strip() if pd.notna(raw_unit) else None
        if unit == "":
            unit = None

        ingredient = Ingredient(
            recipe_id=int(row['recipe_id']),
            ingredient_id=ing_id,
            quantity=quantity,
            unit=unit
        )
        session.add(ingredient)
        recipe_to_ingredient_ids[int(row['recipe_id'])].append(ing_id)

    session.commit()
    return recipe_to_ingredient_ids


def fill_recipe_ingredient_ids_field(session, recipe_to_ingredient_ids: dict[int, list[int]]) -> None:
    for recipe_id, ing_ids in recipe_to_ingredient_ids.items():
        recipe = session.get(Recipe, recipe_id)
        if recipe is not None:
            recipe.ingredient_ids = ','.join(map(str, ing_ids))

    session.commit()


def preview_data(session, limit: int = 5) -> None:
    recipes = session.query(Recipe).all()
    for recipe in recipes[:limit]:
        print(f'\n📌 {recipe.title}')
        print('IDs:', recipe.ingredient_ids)
        for ing in recipe.ingredients:
            ing_name = ing.ingredient_name.name if ing.ingredient_name else 'UNKNOWN'
            print(' -', ing_name, ing.quantity, ing.unit)


def main() -> None:
    validate_files()

    engine, SessionLocal = create_engine_and_session()
    recreate_database(engine)

    recipes_df, ingredients_df = load_dataframes()

    session = SessionLocal()
    try:
        name_to_id = fill_ingredient_names(session, ingredients_df)
        fill_recipes(session, recipes_df)
        recipe_to_ingredient_ids = fill_recipe_ingredients(session, ingredients_df, name_to_id)
        fill_recipe_ingredient_ids_field(session, recipe_to_ingredient_ids)
        preview_data(session)
        print(f'\nБаза успешно создана: {DB_PATH}')
    finally:
        session.close()


if __name__ == '__main__':
    main()
