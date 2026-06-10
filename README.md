# RAG Recipe Assistant

Система поиска кулинарных рецептов с учётом диетических ограничений на основе RAG (Retrieval-Augmented Generation).

## Требования

- Python 3.10+
- uv

## Установка и запуск

```bash
# 1. Клонировать репозиторий
git clone <ваш-репозиторий>
cd <папка-проекта>

# 2. Создать окружение и установить зависимости
uv venv
uv sync

# 3. Подготовить данные (если datasets.json отсутствует)
# Скачайте ZIP с Kaggle: https://www.kaggle.com/datasets/hugodarwood/epirecipes
# Распакуйте full_format_recipes.json в data/raw/
uv run python scripts/prepare_data.py

# 4. Собрать индекс
uv run python scripts/build_index.py

# 5. Запустить UI
uv run streamlit run app/main.py

## Демо-вопросы

| Запрос | Ожидаемый результат |
|--------|---------------------|
| `chicken recipe under 400 calories` | 3 рецепта курицы с калорийностью < 400 |
| `vegetarian breakfast with high protein` | 3 вегетарианских завтрака с высоким белком |
| `quick pasta without cheese` | 3 рецепта пасты без сыра |
| `how to fix a car` | Отказ (некулинарный запрос) |

## Тесты

```bash
uv run pytest tests/ -v


## Структура проекта
├── app/
│ ├── config.py # конфигурация (пути, top_k=3, порог 0.25)
│ ├── chunker.py # нарезка текста на чанки
│ ├── retriever.py # TF-IDF поиск
│ ├── generator.py # формирование ответа
│ ├── prompts.py # правила для demo-режима
│ └── main.py # Streamlit UI
├── scripts/
│ ├── prepare_data.py # подготовка datasets.json из сырых данных
│ └── build_index.py # сборка TF-IDF индекса
├── data/
│ ├── raw/ # исходные даon)
│ ├── processed/ # промежуточные файлы
│ └── index/ # TF-IDF индекс
├── tests/ # тесты
├── doc/ # документация 
├── screenshots/ # скриншоты
└── homework/ # файлы для сдачи

## Документация

- [Идея проекта](doc/00_project_idea.md)
- [Техническое видение](doc/vision.md)
- [Правила разработки](doc/conventions.md)
- [План итераций](doc/tasklist.md)
- [Процесс работы](doc/workflow.md)
- [Описание данных](doc/DATA.md)

## Ограничения

- Поиск только на английском языке
- TF-IDF не понимает синонимы
- При пороге 0.25 возможны редкие ложные срабатывания

## Лицензия

Данные Epicurious предоставлены для образовательных целей.

