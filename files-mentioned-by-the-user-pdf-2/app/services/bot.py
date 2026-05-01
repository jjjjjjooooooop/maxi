from collections.abc import Iterable


RESPONSES: list[tuple[Iterable[str], str]] = [
    (
        ("html", "тег", "страниц"),
        "HTML отвечает за структуру страницы: заголовки, поля ввода, кнопки и область чата.",
    ),
    (
        ("css", "стил", "адаптив"),
        "CSS управляет внешним видом. Для проекта важно использовать переменные, псевдоклассы и адаптивную верстку.",
    ),
    (
        ("javascript", "js", "fetch", "async", "await"),
        "JavaScript обрабатывает отправку формы, вызывает API через fetch и обновляет окно чата без перезагрузки.",
    ),
    (
        ("api", "endpoint", "эндпоинт", "fastapi"),
        "Backend предоставляет REST API: регистрацию, логин, создание сессии, отправку сообщения и историю.",
    ),
    (
        ("jwt", "токен", "авторизац", "логин"),
        "JWT-токен подтверждает пользователя и передается в заголовке Authorization: Bearer TOKEN.",
    ),
    (
        ("sql", "база", "sqlite", "истори"),
        "SQLAlchemy сохраняет пользователей, сессии и оба сообщения каждой пары: вопрос пользователя и ответ бота.",
    ),
]


def build_bot_reply(text: str) -> str:
    normalized = text.lower()
    for keywords, response in RESPONSES:
        if any(keyword in normalized for keyword in keywords):
            return response
    return (
        "Я бот поддержки по веб-разработке. Спросите про HTML, CSS, JavaScript, API, JWT или базу данных."
    )
