# Tasklist — итерационный план разработки

Опирается на: @vision.md · @conventions.md · @00_project_idea.md

## 📊 Отчёт по прогрессу

| Итерация | Название | Статус | Проверка |
|----------|----------|--------|----------|
| 0 | Каркас проекта | ✅ | uv sync без ошибок |
| 1 | Подготовка данных Epicurious | ⬜ | datasets.json с 5000 рецептов |
| 2 | Ingestion | ⬜ | documents.jsonl создан |
| 3 | Chunking | ⬜ | chunks.jsonl, тест chunking |
| 4 | Индекс TF-IDF | ⬜ | файлы в data/index/ |
| 5 | Retrieval | ⬜ | top_k=3 + score в консоли |
| 6 | Demo-ответ | ⬜ | ответ + источники без UI |
| 7 | Streamlit UI | ⬜ | demo-вопросы в браузере |
| 8 | Тесты и README | ⬜ | pytest green, README воспроизводим |

Легенда: ⬜ не начато · 🔄 в работе · ✅ готово · ❌ блокер

Текущая итерация: 1
Готовность MVP: 1 / 9

## Итерация 0 — Каркас проекта

- `pyproject.toml` — зависимости: streamlit, scikit-learn, pytest
- `.gitignore` — `.venv/`, `data/index/`, `__pycache__/`
- Папки: `app/`, `scripts/`, `data/raw/`, `data/processed/`, `data/index/`, `tests/`
- `app/config.py` — пути, top_k=3, размер чанка

**Проверка:**

```bash
uv venv && uv sync
uv run python -c "import app.config"

## Итерация 1 — Подготовка данных Epicurious

- Скачать ZIP с Kaggle (кнопка Download) → распаковать → `full_format_recipes.json` в `data/raw/`
- Создать `scripts/prepare_data.py`:
  - Загрузить `full_format_recipes.json`
  - Взять первые 5000 рецептов
  - Извлечь поля: `title`, `ingredients`, `directions`, `calories`
  - Собрать `text` из названия, ингредиентов и инструкций
  - Сохранить как `data/raw/datasets.json`

**Проверка:**

```bash
uv run python scripts/prepare_data.py
uv run python -c "import json; d=json.load(open('data/raw/datasets.json')); assert len(d) == 5000; print('OK')"

## Итерация 2 — Ingestion

- `scripts/ingest.py` — читает `data/raw/datasets.json` → `data/processed/documents.jsonl`
- Каждый документ: `doc_id`, `text`, `metadata` (калории)

**Проверка:**

```bash
uv run python scripts/ingest.py
# → documents.jsonl, строк = 5000

## Итерация 3 — Chunking

- `app/chunker.py` — нарезка по абзацам, max 400 символов, overlap 50
- Выход: `data/processed/chunks.jsonl`

**Проверка:**

```bash
uv run pytest tests/test_chunking.py -v

## Итерация 4 — Индекс TF-IDF

- `scripts/build_index.py` — ingest + chunk + TF-IDF fit
- Сохранение: `data/index/vectorizer.pkl`, `matrix.npz`, `chunks.jsonl`

**Проверка:**

```bash
uv run python scripts/build_index.py
# → три файла в data/index/

## Итерация 5 — Retrieval

- `app/retriever.py` — загрузка индекса, cosine similarity, top_k=3
- Возврат: `text`, `doc_id`, `score`

**Проверка:**

```bash
uv run python -c "
from app.retriever import Retriever
r = Retriever()
print(r.search('chicken under 400 calories', k=3))
"

## Итерация 6 — Demo-ответ

- `app/prompts.py` — правила: только по контексту, отказ без данных, отказ на некулинарные запросы
- `app/generator.py` — ответ из top_k + список источников

**Проверка:**

```bash
uv run python -c "
from app.generator import ask
print(ask('vegetarian breakfast high protein'))
"
# → текст + sources с doc_id

## Итерация 7 — Streamlit UI

- `app/main.py` — поле вопроса, top-k фрагментов, ответ, источники
- Сообщение, если индекс не собран

**Проверка:**

```bash
uv run streamlit run app/main.py

Demo-вопросы:

"chicken recipe under 400 calories" → ответ + источники
"vegetarian breakfast with high protein" → ответ + источники
"how to fix a car" → отказ

## Итерация 8 — Тесты и README

- `tests/test_chunking.py`, `tests/test_retrieval.py` — 3–5 тестов
- Корневой `README.md` — uv, prepare_data, build_index, streamlit, demo-вопросы

**Проверка:**

```bash
uv run pytest tests/ -v
# README: запуск с нуля на чистой машине

## Критерий «MVP готов»

- Все итерации 0–8 отмечены ✅ в таблице прогресса
- 3 demo-вопроса из `00_project_idea.md` возвращают ответ с источниками:
  - "chicken recipe under 400 calories"
  - "vegetarian breakfast with high protein"
  - "quick pasta without cheese"
- 1 negative-запрос возвращает отказ:
  - "how to fix a car"
- Система запускается командами:
  ```bash
  uv run python scripts/prepare_data.py
  uv run python scripts/build_index.py
  uv run streamlit run app/main.py
