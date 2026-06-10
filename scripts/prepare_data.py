"""Подготовка датасета: первые 5000 рецептов Epicurious → datasets.json."""

import json

from app.config import DATA_RAW, DATASETS_JSON

RECIPES_LIMIT = 5000
SOURCE_FILE = DATA_RAW / "full_format_recipes.json"


def build_text(title: str, ingredients: list, directions: list) -> str:
    parts = [title.strip()]
    if ingredients:
        parts.append("\n".join(ingredients))
    if directions:
        parts.append("\n".join(directions))
    return "\n\n".join(parts)


def is_valid(recipe: dict) -> bool:
    return all(k in recipe for k in ("title", "ingredients", "directions", "calories"))


def prepare_recipe(recipe: dict) -> dict:
    return {
        "title": recipe["title"],
        "ingredients": recipe["ingredients"],
        "directions": recipe["directions"],
        "calories": recipe["calories"],
        "text": build_text(
            recipe["title"],
            recipe.get("ingredients", []),
            recipe.get("directions", []),
        ),
    }


def main() -> None:
    with SOURCE_FILE.open(encoding="utf-8") as f:
        recipes = json.load(f)

    prepared = []
    for recipe in recipes:
        if not is_valid(recipe):
            continue
        prepared.append(prepare_recipe(recipe))
        if len(prepared) == RECIPES_LIMIT:
            break

    DATASETS_JSON.write_text(
        json.dumps(prepared, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Saved {len(prepared)} recipes to {DATASETS_JSON}")


if __name__ == "__main__":
    main()
