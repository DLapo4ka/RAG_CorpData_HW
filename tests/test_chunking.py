from app.chunker import chunk_document, chunk_text, write_chunks_jsonl
from app.config import CHUNK_MAX_CHARS, CHUNK_OVERLAP, CHUNKS_JSONL


def test_short_text_single_chunk():
    text = "Tomato Soup\n\n2 tomatoes\n\n1. Chop tomatoes."
    chunks = chunk_text(text)
    assert len(chunks) == 1
    assert chunks[0] == text


def test_chunks_respect_max_size():
    paragraphs = [f"Paragraph {i}. " + "word " * 40 for i in range(10)]
    text = "\n\n".join(paragraphs)
    chunks = chunk_text(text, max_chars=CHUNK_MAX_CHARS, overlap=CHUNK_OVERLAP)
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk) <= CHUNK_MAX_CHARS


def test_consecutive_chunks_have_overlap():
    paragraphs = [f"Block {i}: " + "x" * 120 for i in range(8)]
    text = "\n\n".join(paragraphs)
    chunks = chunk_text(text, max_chars=CHUNK_MAX_CHARS, overlap=CHUNK_OVERLAP)
    assert len(chunks) >= 2
    for prev, nxt in zip(chunks, chunks[1:]):
        assert prev[-CHUNK_OVERLAP:] == nxt[:CHUNK_OVERLAP]


def test_chunk_document_has_ids():
    document = {
        "doc_id": "recipe_42",
        "text": "Salad\n\ningredient one\ningredient two\n\n1. Mix.",
        "metadata": {"calories": 100},
    }
    chunks = chunk_document(document)
    assert chunks
    assert chunks[0]["chunk_id"] == "recipe_42_0"
    assert chunks[0]["doc_id"] == "recipe_42"
    assert chunks[0]["text"]


def test_write_chunks_jsonl(tmp_path):
    documents_path = tmp_path / "documents.jsonl"
    output_path = tmp_path / "chunks.jsonl"
    documents_path.write_text(
        '{"doc_id": "recipe_0", "text": "A\\n\\nB", "metadata": {"calories": 1.0}}\n',
        encoding="utf-8",
    )

    count = write_chunks_jsonl(documents_path=documents_path, output_path=output_path)

    assert count == 1
    assert output_path.exists()
    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1


def test_write_chunks_from_processed_documents():
    count = write_chunks_jsonl()
    assert count > 0
    lines = CHUNKS_JSONL.read_text(encoding="utf-8").splitlines()
    assert len(lines) == count
    assert all('"chunk_id"' in line and '"doc_id"' in line for line in lines)
