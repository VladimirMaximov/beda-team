import csv

RECIPES_INPUT = "recipes.csv"
INGREDIENTS_INPUT = "recipe_ingredients.csv"

RECIPES_OUTPUT = "recipes_clean.csv"
INGREDIENTS_OUTPUT = "recipe_ingredients_clean.csv"


def is_bad_ingredients(text):

    if text is None:
        return True

    text = text.strip()

    if text == "" or text.lower() == "nan":
        return True

    words = text.split()

    if len(words) == 0:
        return True

    avg_len = sum(len(w) for w in words) / len(words)
    short_ratio = sum(1 for w in words if len(w) <= 2) / len(words)

    if avg_len < 4:
        return True

    if short_ratio > 0.5:
        return True

    return False


def clean_data():

    valid_recipe_ids = set()

    total = 0
    kept = 0
    removed = 0

    # --- ЧИСТИМ recipes.csv ---
    with open(RECIPES_INPUT, encoding="utf-8") as infile, \
         open(RECIPES_OUTPUT, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)

        writer.writeheader()

        for row in reader:

            total += 1

            ingredients_text = row.get("ingredients_text")

            if is_bad_ingredients(ingredients_text):
                removed += 1
                continue

            recipe_id = row["id"]
            valid_recipe_ids.add(recipe_id)

            writer.writerow(row)
            kept += 1

    print("=== RECIPES ===")
    print("Всего:", total)
    print("Оставлено:", kept)
    print("Удалено:", removed)
    print("Процент удалённых:", round(removed / total * 100, 2), "%")

    # --- ЧИСТИМ recipe_ingredients.csv ---
    ing_total = 0
    ing_kept = 0
    ing_removed = 0

    with open(INGREDIENTS_INPUT, encoding="utf-8") as infile, \
         open(INGREDIENTS_OUTPUT, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)

        writer.writeheader()

        for row in reader:

            ing_total += 1

            recipe_id = row["recipe_id"]

            if recipe_id not in valid_recipe_ids:
                ing_removed += 1
                continue

            writer.writerow(row)
            ing_kept += 1

    print("\n=== INGREDIENTS ===")
    print("Всего:", ing_total)
    print("Оставлено:", ing_kept)
    print("Удалено:", ing_removed)
    print("Процент удалённых:", round(ing_removed / ing_total * 100, 2), "%")


if __name__ == "__main__":
    clean_data()