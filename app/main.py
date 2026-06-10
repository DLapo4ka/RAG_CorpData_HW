"""Streamlit UI для RAG-помощника по рецептам."""

import streamlit as st

from app.config import INDEX_CHUNKS_JSONL, MATRIX_NPZ, TOP_K, VECTORIZER_PKL
from app.generator import ask, get_retriever

INDEX_MISSING_MESSAGE = (
    "Индекс не собран. Выполните команду:\n\n"
    "`uv run python scripts/build_index.py`"
)

DEMO_QUESTIONS = (
    "chicken recipe under 400 calories",
    "vegetarian breakfast with high protein",
    "how to fix a car",
)


def index_ready() -> bool:
    return all(path.exists() for path in (VECTORIZER_PKL, MATRIX_NPZ, INDEX_CHUNKS_JSONL))


st.set_page_config(page_title="Recipe RAG", page_icon="🍳")
st.title("Recipe RAG — помощник по рецептам")
st.caption("Demo-режим: ответ только из найденных фрагментов рецептов.")

if not index_ready():
    st.error(INDEX_MISSING_MESSAGE)
    st.stop()

if "query" not in st.session_state:
    st.session_state.query = ""

with st.sidebar:
    st.header("Demo-вопросы")
    for index, question in enumerate(DEMO_QUESTIONS):
        if st.button(question, key=f"demo_{index}", use_container_width=True):
            st.session_state.query = question

query = st.text_input(
    "Ваш вопрос",
    key="query",
    placeholder="chicken recipe under 400 calories",
)
search = st.button("Найти рецепты", type="primary")

if search and query.strip():
    hits = get_retriever().search(query.strip(), k=TOP_K)

    st.subheader("Найденные фрагменты")
    for index, hit in enumerate(hits, start=1):
        with st.expander(f"{index}. {hit['doc_id']} — score {hit['score']:.3f}"):
            st.text(hit["text"])

    result = ask(query.strip())

    st.subheader("Ответ")
    st.write(result["answer"])

    if result["sources"]:
        st.subheader("Источники")
        for source in result["sources"]:
            st.markdown(
                f"**{source['title']}** — `{source['doc_id']}` "
                f"(score: {source['score']:.3f})"
            )
            st.caption(source["nutrition_text"])
            st.text(source["text"])
