"""Нарезка документов на чанки по абзацам."""

import json
from pathlib import Path

from app.config import CHUNK_MAX_CHARS, CHUNK_OVERLAP, CHUNKS_JSONL, DOCUMENTS_JSONL

PARAGRAPH_SEP = "\n\n"


def split_paragraphs(text: str) -> list[str]:
    paragraphs = [p.strip() for p in text.split(PARAGRAPH_SEP) if p.strip()]
    if not paragraphs and text.strip():
        paragraphs = [text.strip()]
    return paragraphs


def split_long_paragraph(paragraph: str, max_chars: int, overlap: int) -> list[str]:
    if len(paragraph) <= max_chars:
        return [paragraph]

    parts = []
    start = 0
    step = max(max_chars - overlap, 1)
    while start < len(paragraph):
        parts.append(paragraph[start : start + max_chars])
        start += step
    return parts


def pack_units(units: list[str], max_chars: int) -> list[str]:
    if not units:
        return []

    packed: list[str] = []
    current: list[str] = []
    current_len = 0

    for unit in units:
        extra = len(PARAGRAPH_SEP) if current else 0
        if current and current_len + extra + len(unit) > max_chars:
            packed.append(PARAGRAPH_SEP.join(current))
            current = [unit]
            current_len = len(unit)
            continue

        if current:
            current_len += extra + len(unit)
        else:
            current_len = len(unit)
        current.append(unit)

    if current:
        packed.append(PARAGRAPH_SEP.join(current))

    return packed


def apply_overlap(chunks: list[str], max_chars: int, overlap: int) -> list[str]:
    if overlap <= 0 or len(chunks) <= 1:
        return chunks

    result = [chunks[0]]
    for chunk in chunks[1:]:
        prefix = result[-1][-overlap:]
        merged = prefix + chunk
        if len(merged) > max_chars:
            merged = prefix + chunk[: max_chars - len(prefix)]
        result.append(merged)
    return result


def chunk_text(
    text: str,
    max_chars: int = CHUNK_MAX_CHARS,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    paragraphs = split_paragraphs(text)
    if not paragraphs:
        return []

    units: list[str] = []
    for paragraph in paragraphs:
        units.extend(split_long_paragraph(paragraph, max_chars, overlap))

    packed = pack_units(units, max_chars)
    return apply_overlap(packed, max_chars, overlap)


def chunk_document(document: dict) -> list[dict]:
    doc_id = document["doc_id"]
    chunks = chunk_text(document["text"])
    return [
        {
            "chunk_id": f"{doc_id}_{index}",
            "doc_id": doc_id,
            "text": chunk,
        }
        for index, chunk in enumerate(chunks)
    ]


def load_documents(path: Path = DOCUMENTS_JSONL) -> list[dict]:
    documents = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            documents.append(json.loads(line))
    return documents


def chunk_documents(documents: list[dict]) -> list[dict]:
    chunks: list[dict] = []
    for document in documents:
        chunks.extend(chunk_document(document))
    return chunks


def write_chunks_jsonl(
    documents_path: Path = DOCUMENTS_JSONL,
    output_path: Path = CHUNKS_JSONL,
) -> int:
    chunks = chunk_documents(load_documents(documents_path))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=True) + "\n")
    return len(chunks)
