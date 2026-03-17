import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv
import re
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

STOPWORDS = {
    "молотый",
    "молотая",
    "свежий",
    "свежая",
    "свежие",
    "твердый",
    "твёрдый",
    "полутвердый",
    "полутвёрдый",
    "рафинированное",
    "растительное"
}


BASE_URL = "https://www.russianfood.com/recipes/recipe.php?rid="
CONCURRENT_REQUESTS = 10

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

recipes_file = open("recipes.csv", "w", newline="", encoding="utf-8")
ingredients_file = open("recipe_ingredients.csv", "w", newline="", encoding="utf-8")

recipes_writer = csv.writer(recipes_file)
ingredients_writer = csv.writer(ingredients_file)

recipes_writer.writerow([
    "id",
    "title",
    "instructions",
    "url",
    "source",
    "ingredients_text"
])

ingredients_writer.writerow([
    "recipe_id",
    "ingredient",
    "quantity",
    "unit"
])

recipe_counter = 1



def normalize_ingredient(name):

    # lowercase
    name = name.lower()

    # удалить текст в скобках
    name = re.sub(r"\(.*?\)", "", name)

    # удалить лишние символы
    name = re.sub(r"[^а-яё\s]", "", name)

    words = name.split()

    normalized_words = []

    for w in words:

        if w in STOPWORDS:
            continue

        p = morph.parse(w)[0]

        lemma = p.normal_form

        normalized_words.append(lemma)

    return " ".join(normalized_words)



def parse_recipe(html):

    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.find("h1")
    if not title_tag:
        return None

    title = title_tag.get_text(strip=True)

    ingredients = []

    table = soup.find("table", class_="ingr")

    if table:

        rows = table.find_all("tr")

        for row in rows[1:]:

            cols = row.find_all("td")

            if len(cols) < 3:
                continue

            name = cols[0].get_text(strip=True)
            quantity = cols[1].get_text(strip=True)
            unit = cols[2].get_text(strip=True)

            name = normalize_ingredient(name)

            ingredients.append({
                "ingredient": name,
                "quantity": quantity,
                "unit": unit
            })

    instructions = []

    how_block = soup.find("div", id="how")

    if how_block:

        paragraphs = how_block.find_all("p")

        for p in paragraphs:

            text = p.get_text(" ", strip=True)

            if text:
                instructions.append(text)

    return {
        "title": title,
        "ingredients": ingredients,
        "instructions": instructions
    }


def generate_ingredients_text(ingredients):

    return " ".join(
        ing["ingredient"]
        for ing in ingredients
    )


async def fetch(session, rid):

    url = BASE_URL + str(rid)

    try:

        async with session.get(url) as response:

            if response.status != 200:
                return None

            html = await response.text()

            recipe = parse_recipe(html)

            if recipe:

                recipe["url"] = url

                return recipe

    except:
        return None


async def worker(session, queue):

    global recipe_counter

    while True:

        rid = await queue.get()

        recipe = await fetch(session, rid)

        if recipe:

            recipe_id = recipe_counter
            recipe_counter += 1

            instructions_text = "\n".join(recipe["instructions"])

            ingredients_text = generate_ingredients_text(
                recipe["ingredients"]
            )

            recipes_writer.writerow([
                recipe_id,
                recipe["title"],
                instructions_text,
                recipe["url"],
                "russianfood",
                ingredients_text
            ])

            for ing in recipe["ingredients"]:

                ingredients_writer.writerow([
                    recipe_id,
                    ing["ingredient"],
                    ing["quantity"],
                    ing["unit"]
                ])

            print("saved:", recipe["title"])

        queue.task_done()


async def main(start=1, end=200):

    queue = asyncio.Queue()

    for rid in range(start, end):
        await queue.put(rid)

    async with aiohttp.ClientSession(headers=HEADERS) as session:

        tasks = []

        for _ in range(CONCURRENT_REQUESTS):

            tasks.append(
                asyncio.create_task(worker(session, queue))
            )

        await queue.join()

        for t in tasks:
            t.cancel()


if __name__ == "__main__":
    asyncio.run(main(1, 600_000))


recipes_file.close()
ingredients_file.close()