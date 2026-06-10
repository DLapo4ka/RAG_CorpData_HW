# Recipe RAG — учебный помощник по рецептам

Локальный RAG на датасете Epicurious (Kaggle): TF-IDF поиск, demo-ответ из найденных чанков, Streamlit UI.

## Требования

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

## Установка

```bash
uv venv
uv sync
```

## Данные

1. Скачайте [Epicurious Recipes](https://www.kaggle.com/datasets/hugodarwood/epirecipes) с Kaggle.
2. Распакуйте `full_format_recipes.json` в `data/raw/`.

## Подготовка и индекс

```bash
uv run python scripts/prepare_data.py
uv run python scripts/build_index.py
```

`build_index.py` выполняет ingest, chunking и сборку TF-IDF индекса в `data/index/`.

## Запуск UI

```bash
uv run streamlit run app/main.py
```

## Demo-вопросы

Должны вернуть ответ с источниками:

- `chicken recipe under 400 calories`
- `vegetarian breakfast with high protein`
- `quick pasta without cheese`

Должен вернуть отказ:

- `how to fix a car`

## Тесты

```bash
uv run pytest tests/ -v
```

## Структура

| Путь | Назначение |
|------|------------|
| `app/config.py` | Пути, `TOP_K`, `MIN_SCORE`, размер чанка |
| `app/chunker.py` | Нарезка по абзацам |
| `app/retriever.py` | TF-IDF поиск |
| `app/generator.py` | Demo-ответ |
| `app/main.py` | Streamlit UI |
| `scripts/` | Подготовка данных и сборка индекса |
| `data/index/` | `vectorizer.pkl`, `matrix.npz`, `chunks.jsonl` |

Подробнее: `doc/vision.md`, `doc/tasklist.md`.
