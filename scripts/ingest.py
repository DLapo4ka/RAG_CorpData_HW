"""Ingestion: datasets.json → documents.jsonl."""

import json

from app.config import DATASETS_JSON, DOCUMENTS_JSONL


def to_document(index: int, recipe: dict) -> dict:
    return {
        "doc_id": f"recipe_{index}",
        "text": recipe["text"],
        "metadata": {"calories": recipe["calories"]},
    }


def main() -> None:
    with DATASETS_JSON.open(encoding="utf-8") as f:
        recipes = json.load(f)

    with DOCUMENTS_JSONL.open("w", encoding="utf-8") as f:
        for i, recipe in enumerate(recipes):
            f.write(json.dumps(to_document(i, recipe), ensure_ascii=False) + "\n")

    print(f"Saved {len(recipes)} documents to {DOCUMENTS_JSONL}")


if __name__ == "__main__":
    main()
