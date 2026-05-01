# Чат-бот поддержки

Проект выполнен по двум навигационным листам итоговой аттестации: frontend на HTML/CSS/JavaScript и backend на FastAPI с SQLAlchemy, Alembic, JWT и тестами.

## Возможности

- регистрация и авторизация пользователей;
- JWT-защита API;
- создание чат-сессии;
- отправка сообщений в чат;
- генерация ответа бота по ключевым словам;
- сохранение пользовательских и ответных сообщений в SQLite;
- получение истории переписки;
- frontend с `fetch`, `async/await`, `localStorage`, валидацией формы, индикатором «бот печатает» и очисткой окна чата.

## Установка и запуск

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

После запуска откройте:

- приложение: http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs

В этой папке Codex зависимости уже установлены локально в `.deps`. Если нужно запустить без виртуального окружения:

```powershell
$env:PYTHONPATH=(Resolve-Path '.deps').Path + ';' + (Get-Location).Path
python -m uvicorn app.main:app --reload
```

## Тестирование

```bash
pytest
```

Тесты используют временную SQLite-базу и проверяют регистрацию, логин, создание сессии, отправку сообщения, сохранение пары сообщений и получение истории.

## Основные API-запросы

Регистрация:

```bash
curl -X POST http://127.0.0.1:8000/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"student\",\"password\":\"password123\"}"
```

Логин:

```bash
curl -X POST http://127.0.0.1:8000/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"student\",\"password\":\"password123\"}"
```

Создание сессии:

```bash
curl -X POST http://127.0.0.1:8000/chat/session ^
  -H "Authorization: Bearer TOKEN"
```

Отправка сообщения:

```bash
curl -X POST http://127.0.0.1:8000/chat/message ^
  -H "Authorization: Bearer TOKEN" ^
  -H "Content-Type: application/json" ^
  -d "{\"session_id\":1,\"text\":\"Как подключить CSS?\"}"
```

История:

```bash
curl http://127.0.0.1:8000/chat/history/1 ^
  -H "Authorization: Bearer TOKEN"
```

## Структура

```text
app/
  api/           маршруты auth и chat
  core/          настройки и безопасность
  db/            подключение к базе
  models/        SQLAlchemy-модели
  schemas/       Pydantic-схемы
  services/      логика бота
  static/        frontend
tests/           автоматизированные тесты
alembic/         миграции базы данных
```
