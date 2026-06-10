"""Проверка порога релевантности MIN_SCORE в demo-ответе."""

from app.config import MIN_SCORE, TOP_K
from app.generator import ask
from app.prompts import REFUSAL_NO_CONTEXT
from app.retriever import Retriever


def test_min_score_config_value():
    assert MIN_SCORE == 0.25


def test_all_returned_sources_meet_min_score():
    queries_with_answer = (
        "chicken breast",
        "quick breakfast eggs",
        "vegetarian soup",
    )
    for query in queries_with_answer:
        result = ask(query)
        assert result["sources"], f"expected sources for: {query}"
        for source in result["sources"]:
            assert source["score"] >= MIN_SCORE


def test_all_hits_below_min_score_returns_refusal():
    query = "healthy meal"
    retriever = Retriever()
    hits = retriever.search(query, k=TOP_K)

    assert hits
    assert max(hit["score"] for hit in hits) < MIN_SCORE

    result = ask(query)
    assert result["sources"] == []
    assert result["answer"] == REFUSAL_NO_CONTEXT


def test_hits_below_min_score_excluded_from_sources():
    query = "quick breakfast eggs"
    retriever = Retriever()
    hits = retriever.search(query, k=TOP_K)
    result = ask(query)

    above_threshold = [hit for hit in hits if hit["score"] >= MIN_SCORE]
    below_threshold = [hit for hit in hits if hit["score"] < MIN_SCORE]

    assert above_threshold
    assert below_threshold
    assert len(result["sources"]) == len(above_threshold)
    assert len(result["sources"]) < len(hits)

    returned_scores = {round(source["score"], 6) for source in result["sources"]}
    for hit in below_threshold:
        assert round(hit["score"], 6) not in returned_scores
