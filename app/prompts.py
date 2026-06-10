"""Правила demo-режима: ответ только по найденному контексту."""

REFUSAL_NO_CONTEXT = (
    "Не нашёл подходящих рецептов по вашему запросу. "
    "Попробуйте переформулировать вопрос на английском."
)

REFUSAL_OFF_TOPIC = (
    "Это не кулинарный запрос. Задайте вопрос о рецептах, ингредиентах или калориях."
)

REFUSAL_NO_RUSSIAN = (
    "В базе только рецепты на английском. Задайте вопрос на английском языке."
)

OFF_TOPIC_KEYWORDS = (
    "car",
    "automobile",
    "engine",
    "repair",
    "fix a",
    "exchange rate",
    "dollar",
    "stock market",
    "computer",
    "programming",
    "bitcoin",
)

CULINARY_KEYWORDS = (
    "recipe",
    "cook",
    "food",
    "meal",
    "breakfast",
    "lunch",
    "dinner",
    "ingredient",
    "calorie",
    "calories",
    "vegetarian",
    "vegan",
    "chicken",
    "pasta",
    "soup",
    "salad",
    "protein",
    "bake",
    "grill",
    "sauce",
    "dish",
)
