"""Поиск релевантных чанков по TF-IDF индексу."""

import json
import pickle

import scipy.sparse
from sklearn.metrics.pairwise import cosine_similarity

from app.config import (
    INDEX_CHUNKS_JSONL,
    MATRIX_NPZ,
    TOP_K,
    VECTORIZER_PKL,
)


def load_chunks(path=INDEX_CHUNKS_JSONL) -> list[dict]:
    chunks = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks


class Retriever:
    def __init__(
        self,
        vectorizer_path=VECTORIZER_PKL,
        matrix_path=MATRIX_NPZ,
        chunks_path=INDEX_CHUNKS_JSONL,
    ):
        if not vectorizer_path.exists():
            raise FileNotFoundError(f"Индекс не найден: {vectorizer_path}")
        if not matrix_path.exists():
            raise FileNotFoundError(f"Индекс не найден: {matrix_path}")
        if not chunks_path.exists():
            raise FileNotFoundError(f"Индекс не найден: {chunks_path}")

        with vectorizer_path.open("rb") as f:
            self.vectorizer = pickle.load(f)
        self.matrix = scipy.sparse.load_npz(matrix_path)
        self.chunks = load_chunks(chunks_path)

    def search(self, query: str, k: int = TOP_K) -> list[dict]:
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix).flatten()
        top_indices = scores.argsort()[-k:][::-1]

        results = []
        for index in top_indices:
            chunk = self.chunks[index]
            results.append(
                {
                    "text": chunk["text"],
                    "doc_id": chunk["doc_id"],
                    "score": float(scores[index]),
                }
            )
        return results
