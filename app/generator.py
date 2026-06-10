"""Demo-генератор ответа из найденных чанков без LLM."""

import json

from app.config import DATASETS_JSON, MIN_SCORE, TOP_K
from app.prompts import (
    CULINARY_KEYWORDS,
    OFF_TOPIC_KEYWORDS,
    REFUSAL_NO_CONTEXT,
    REFUSAL_NO_RUSSIAN,
    REFUSAL_OFF_TOPIC,
)
from app.retriever import Retriever

_retriever: Retriever | None = None
_recipes_by_id: dict[str, dict] | None = None


def get_retriever() -> Retriever:
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever


def get_recipes_by_id() -> dict[str, dict]:
    global _recipes_by_id
    if _recipes_by_id is None:
        with DATASETS_JSON.open(encoding="utf-8") as f:
            recipes = json.load(f)
        _recipes_by_id = {
            f"recipe_{index}": recipe for index, recipe in enumerate(recipes)
        }
    return _recipes_by_id


def get_recipe(doc_id: str) -> dict:
    return get_recipes_by_id().get(doc_id, {})


def get_recipe_title(doc_id: str, chunk_text: str = "") -> str:
    title = get_recipe(doc_id).get("title", "").strip()
    if title:
        return title
    return chunk_text.split("\n\n", 1)[0].strip() or doc_id


def get_recipe_nutrition(doc_id: str) -> dict:
    recipe = get_recipe(doc_id)
    return {
        "calories": recipe.get("calories"),
        "protein": recipe.get("protein"),
        "fat": recipe.get("fat"),
    }


def format_nutrition(nutrition: dict) -> str:
    labels = (
        ("calories", "Калории", "kcal"),
        ("protein", "Белки", "g"),
        ("fat", "Жиры", "g"),
    )
    parts = []
    for key, label, unit in labels:
        value = nutrition.get(key)
        if value is None:
            parts.append(f"{label}: н/д")
        else:
            parts.append(f"{label}: {value:.0f} {unit}")
    return ", ".join(parts)


def has_cyrillic(text: str) -> bool:
    return any("\u0400" <= char <= "\u04ff" for char in text)


def is_off_topic(query: str) -> bool:
    lowered = query.lower()
    if any(keyword in lowered for keyword in OFF_TOPIC_KEYWORDS):
        if not any(keyword in lowered for keyword in CULINARY_KEYWORDS):
            return True
    return False


def build_answer(chunks: list[dict]) -> str:
    lines = ["Here are relevant recipes from the database:\n"]
    for index, chunk in enumerate(chunks, start=1):
        title = get_recipe_title(chunk["doc_id"], chunk["text"])
        nutrition = format_nutrition(get_recipe_nutrition(chunk["doc_id"]))
        lines.append(f"{index}. {title}")
        lines.append(f"   {nutrition}")
        lines.append(f"   {chunk['text'].strip()}")
    return "\n".join(lines)


def to_sources(chunks: list[dict]) -> list[dict]:
    sources = []
    for chunk in chunks:
        nutrition = get_recipe_nutrition(chunk["doc_id"])
        sources.append(
            {
                "doc_id": chunk["doc_id"],
                "title": get_recipe_title(chunk["doc_id"], chunk["text"]),
                "nutrition": nutrition,
                "nutrition_text": format_nutrition(nutrition),
                "text": chunk["text"],
                "score": chunk["score"],
            }
        )
    return sources


def refuse(message: str) -> dict:
    return {"answer": message, "sources": []}


def ask(query: str) -> dict:
    query = query.strip()
    if not query:
        return refuse(REFUSAL_NO_CONTEXT)

    if has_cyrillic(query):
        return refuse(REFUSAL_NO_RUSSIAN)

    if is_off_topic(query):
        return refuse(REFUSAL_OFF_TOPIC)

    chunks = get_retriever().search(query, k=TOP_K)
    relevant = [chunk for chunk in chunks if chunk["score"] >= MIN_SCORE]
    if not relevant:
        return refuse(REFUSAL_NO_CONTEXT)

    return {
        "answer": build_answer(relevant),
        "sources": to_sources(relevant),
    }
