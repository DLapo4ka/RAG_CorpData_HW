from app.config import MIN_SCORE, TOP_K
from app.generator import ask
from app.retriever import Retriever


def test_search_returns_k_results():
    retriever = Retriever()
    results = retriever.search("chicken pasta", k=TOP_K)
    assert len(results) == TOP_K
    for item in results:
        assert set(item) == {"text", "doc_id", "score"}
        assert item["doc_id"].startswith("recipe_")


def test_search_results_sorted_by_score():
    retriever = Retriever()
    results = retriever.search("tomato soup", k=TOP_K)
    scores = [item["score"] for item in results]
    assert scores == sorted(scores, reverse=True)


def test_ask_sources_contain_doc_id():
    result = ask("vegetarian soup")
    assert result["sources"]
    for source in result["sources"]:
        assert "doc_id" in source
        assert source["score"] >= MIN_SCORE


def test_sources_include_title_and_full_text():
    result = ask("chicken breast")
    assert result["sources"]
    for source in result["sources"]:
        assert source["title"]
        assert source["text"]
        assert source["title"] in result["answer"]


def test_sources_include_nutrition():
    result = ask("vegetarian soup")
    assert result["sources"]
    for source in result["sources"]:
        assert "nutrition" in source
        assert "nutrition_text" in source
        assert "Калории:" in source["nutrition_text"]
        assert "Белки:" in source["nutrition_text"]
        assert "Жиры:" in source["nutrition_text"]
        assert source["nutrition_text"] in result["answer"]
    assert any(source["nutrition"]["calories"] is not None for source in result["sources"])


def test_off_topic_refusal():
    result = ask("how to fix a car")
    assert result["sources"] == []
    assert "кулинар" in result["answer"].lower()


def test_mvp_demo_queries_return_sources():
    for query in (
        "chicken recipe under 400 calories",
        "vegetarian breakfast with high protein",
        "quick pasta without cheese",
    ):
        result = ask(query)
        assert result["sources"], f"no sources for: {query}"
