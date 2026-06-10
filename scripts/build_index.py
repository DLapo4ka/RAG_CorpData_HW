"""Сборка TF-IDF индекса: ingest → chunk → fit → save."""

import importlib.util
import json
import pickle
from pathlib import Path

import scipy.sparse
from sklearn.feature_extraction.text import TfidfVectorizer

from app.chunker import load_documents, write_chunks_jsonl
from app.config import (
    DATA_INDEX,
    DOCUMENTS_JSONL,
    INDEX_CHUNKS_JSONL,
    MATRIX_NPZ,
    VECTORIZER_PKL,
)


def _load_script_module(filename: str):
    path = Path(__file__).resolve().parent / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_chunks(path: Path = INDEX_CHUNKS_JSONL) -> list[dict]:
    chunks = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks


def build_index() -> None:
    DATA_INDEX.mkdir(parents=True, exist_ok=True)

    ingest = _load_script_module("ingest.py")
    ingest.main()

    chunk_count = write_chunks_jsonl(
        documents_path=DOCUMENTS_JSONL,
        output_path=INDEX_CHUNKS_JSONL,
    )
    chunks = load_chunks()

    texts = [chunk["text"] for chunk in chunks]
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(texts)

    with VECTORIZER_PKL.open("wb") as f:
        pickle.dump(vectorizer, f)
    scipy.sparse.save_npz(MATRIX_NPZ, matrix)

    doc_count = len(load_documents())
    print(f"Ingested {doc_count} documents")
    print(f"Indexed {chunk_count} chunks")
    print(f"Saved {VECTORIZER_PKL.name}, {MATRIX_NPZ.name}, {INDEX_CHUNKS_JSONL.name}")


if __name__ == "__main__":
    build_index()
