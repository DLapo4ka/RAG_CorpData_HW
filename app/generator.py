"""Demo-генератор ответа из найденных чанков без LLM."""

from app.config import MIN_SCORE, TOP_K
from app.prompts import (
    CULINARY_KEYWORDS,
    OFF_TOPIC_KEYWORDS,
    REFUSAL_NO_CONTEXT,
    REFUSAL_NO_RUSSIAN,
    REFUSAL_OFF_TOPIC,
)
from app.retriever import Retriever

_retriever: Retriever | None = None


def get_retriever() -> Retriever:
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever


def has_cyrillic(text: str) -> bool:
    return any("\u0400" <= char <= "\u04ff" for char in text)


def is_off_topic(query: str) -> bool:
    lowered = query.lower()
    if any(keyword in lowered for keyword in OFF_TOPIC_KEYWORDS):
        if not any(keyword in lowered for keyword in CULINARY_KEYWORDS):
            return True
    return False


def extract_title(chunk_text: str) -> str:
    return chunk_text.split("\n\n", 1)[0].strip()


def build_answer(chunks: list[dict]) -> str:
    lines = ["Here are relevant recipes from the database:\n"]
    for index, chunk in enumerate(chunks, start=1):
        title = extract_title(chunk["text"])
        lines.append(f"{index}. {title}")
    return "\n".join(lines)


def to_sources(chunks: list[dict]) -> list[dict]:
    return [
        {
            "doc_id": chunk["doc_id"],
            "text": chunk["text"],
            "score": chunk["score"],
        }
        for chunk in chunks
    ]


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
