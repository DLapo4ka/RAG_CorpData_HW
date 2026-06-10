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
    # транспорт и ремонт
    "car",
    "automobile",
    "engine",
    "repair",
    "fix a",
    "tire",
    "brake",
    "motorcycle",
    "driving license",
    "gasoline",
    "petrol",
    # финансы и экономика
    "exchange rate",
    "dollar",
    "stock market",
    "bitcoin",
    "cryptocurrency",
    "investment",
    "mortgage",
    "tax return",
    "salary",
    "inflation rate",
    # технологии
    "computer",
    "programming",
    "python code",
    "javascript",
    "software",
    "laptop",
    "smartphone",
    "internet",
    "website",
    "database",
    # погода
    "weather",
    "forecast",
    "temperature today",
    # спорт
    "football",
    "soccer",
    "basketball",
    "world cup",
    "championship",
    "olympics",
    # здоровье (не диета)
    "hospital",
    "medicine",
    "doctor appointment",
    "surgery",
    "vaccine",
    "prescription",
    # образование и работа
    "homework",
    "university",
    "exam",
    "school",
    "job interview",
    "resume",
    # политика и новости
    "election",
    "president",
    "government",
    "politics",
    # путешествия (не еда)
    "flight booking",
    "passport",
    "visa",
    "hotel reservation",
    # развлечения
    "movie",
    "cinema",
    "concert",
    "video game",
    "netflix",
    # география и страны
    "capital of",
    "capital city",
    "population of",
    "which country",
    "geography",
    "continent",
    "border between",
    "largest city in",
    # математика и информатика
    "graph theory",
    "similarities in graph",
    "directed graph",
    "undirected graph",
    "adjacency",
    "vertex",
    "vertices",
    "algorithm",
    "mathematics",
    "calculus",
    "algebra",
    "geometry",
    "equation",
    "theorem",
    "probability",
    "combinatorics",
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
