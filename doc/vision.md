# Vision — техническое видение проекта

Идея продукта: doc/00_project_idea.md
RAG-помощник по кулинарным рецептам с учётом диетических ограничений и питательной ценности.

## 1. Технологии

| Слой | Выбор | Комментарий |
|------|-------|-------------|
| Язык | Python 3.10+ | — |
| Окружение | uv + .venv | uv sync |
| UI | Streamlit | Один entry point |
| Поиск | TF-IDF + cosine similarity | scikit-learn |
| Индекс | Локальные файлы (data/index/) | vectorizer.pkl + matrix.npz |
| LLM | Только demo-режим | Ответ из найденных чанков |
| Данные | Epicurious Recipes (Kaggle) | 5000 рецептов |

## 2. Как строится индекс

1. Загружаем `data/raw/datasets.json`
2. Применяем `TfidfVectorizer` из scikit-learn
3. Сохраняем `vectorizer.pkl` и `matrix.npz` в `data/index/`

## 3. Как работает поиск

1. Пользователь вводит запрос в Streamlit
2. Векторизуем запрос через сохранённый `vectorizer.pkl`
3. Считаем косинусную близость с `matrix.npz`
4. Возвращаем `top_k=3` чанка с `score > 0.25`
5. Demo-генератор формирует ответ с источниками

### Ограничения TF-IDF

Поиск по ключевым словам: синонимы и перефразировки могут не находиться. Для учебного MVP это приемлемо — pipeline тот же, что и с embeddings.

Редкие некулинарные запросы, содержащие общие слова (например, «cup»), могут давать ложные срабатывания при пороге 0.25. Для учебного MVP это приемлемо.

## 4. Что не используем в MVP

ChromaDB, sentence-transformers, torch, LangChain, FastAPI, Docker, reranking, hybrid search, OpenAI, реальная LLM, Kaggle API, pandas для анализа CSV, pip/poetry/conda (используем uv).

## 5. Как запускать проект

```bash
uv venv
uv sync
uv run python scripts/build_index.py
uv run streamlit run app/main.py
