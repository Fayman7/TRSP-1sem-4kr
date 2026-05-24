# FastAPI учебный проект

## Быстрый старт

Все команды — из корня проекта `fastapi-alembic-products`.

### 1. Установка зависимостей

```powershell
cd fastapi-alembic-products
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Переменные окружения (опционально)

```powershell
copy .env.example .env
```

По умолчанию приложение работает **без** `.env` (SQLite `products.db` в корне). Секреты в репозиторий не входят.

### 3. Миграции и начальные данные

Миграции уже в репозитории (`alembic/versions/`). Нужно только применить их и заполнить БД:

```powershell
alembic upgrade head
python scripts\seed_products.py
python scripts\verify_db.py
```

Ожидаемый вывод `verify_db.py`: колонки `id`, `title`, `price`, `count`, `description` и 2 строки.

### 4. Запуск приложения

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- **Документация API (Swagger):** http://127.0.0.1:8000/docs  
- **ReDoc:** http://127.0.0.1:8000/redoc  
- **Health:** http://127.0.0.1:8000/health  

Остановка: `Ctrl+C`.

---

## Проверка основной функциональности

| Блок | Что проверить | Как |
|------|----------------|-----|
| БД + миграции | Таблица `products` | `python scripts\verify_db.py` |
| Товары (SQLAlchemy) | Список товаров | `GET /products` в Swagger |
| Кастомные ошибки | 404 / 400 | `GET /products/9999`, `GET /products/1/reserve?quantity=1000` |
| Валидация JSON | 422 | `POST /users/register` с неверным `age` или `email` |
| In-memory records | CRUD в памяти | `POST/GET/DELETE /records/` в Swagger |
| In-memory users | CRUD в памяти | `POST/GET/DELETE /users` в Swagger |

### Примеры запросов (PowerShell)

**Валидация пользователя (успех):**

```powershell
$body = @{ username="alice"; age=25; email="alice@example.com"; password="secret123" } | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:8000/users/register -Method Post -ContentType "application/json" -Body $body
```

**In-memory пользователь:**

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/users -Method Post -ContentType "application/json" -Body '{"username":"bob","age":30}'
```

---

## Тестирование (ключевые команды)

Перед тестами: `pip install -r requirements.txt` (pytest и др. уже в `requirements.txt`).

| Сценарий | Команда |
|----------|---------|
| **Все pytest-тесты** | `pytest tests/ -v` |
| Синхронные тесты `/records` | `pytest tests/test_records_api.py -v` |
| Асинхронные тесты `/users` | `pytest tests/test_users_async.py -v` |
| Обработка CustomExceptionA/B | `python scripts\test_error_handling.py` |
| Валидация `User` | `python scripts\test_validation.py` |

Ожидаемый результат: все тесты **passed** (21 тест в `tests/` + скрипты без ошибок).

---

## Структура проекта

```
fastapi-alembic-products/
├── app/
│   ├── main.py              # FastAPI, роуты
│   ├── database.py          # SQLAlchemy engine
│   ├── models.py            # Product
│   ├── config.py            # DATABASE_URL из .env
│   ├── exceptions.py        # CustomExceptionA/B
│   ├── error_handlers.py    # обработчики + валидация 422
│   ├── store.py             # in-memory /records
│   ├── users_store.py       # in-memory /users
│   ├── routers/
│   └── schemas/
├── alembic/                 # миграции
├── tests/                   # pytest
├── scripts/                 # seed, verify, вспомогательные проверки
├── requirements.txt
├── pytest.ini
├── alembic.ini
├── .env.example
└── .gitignore               # включает .env, products.db, .venv
```

---

## Миграции Alembic (справка)

Уже созданы две ревизии:

1. `55529bc3b261` — таблица `products`
2. `5b372d90887c` — поле `description`

```powershell
alembic current          # текущая версия
alembic upgrade head     # применить все
alembic downgrade -1     # откат на одну (при необходимости)
```

---

## API по модулям заданий

### Товары (БД)

- `GET /products` — список
- `GET /products/{id}` — один товар (404 если нет)
- `GET /products/{id}/reserve?quantity=N` — резерв (400 если мало на складе)

### Регистрация с валидацией

- `POST /users/register` — модель `User` (`username`, `age` > 18, `email`, `password` 8–16 символов, `phone`)

### In-memory

- `POST/GET/DELETE /records/` — `username`, `email`
- `POST/GET/DELETE /users` — `username`, `age` (DELETE → 204)

### Ошибки

Формат кастомных ошибок: `error_code`, `message`, `status_code`.  
Валидация: `error_code: validation_error`, массив `details`.

---

## Устранение неполадок

| Проблема | Решение |
|----------|---------|
| `ModuleNotFoundError: app` | Запускайте команды из корня проекта; для pytest настроен `pythonpath = .` в `pytest.ini` |
| Пустой `/products` | `alembic upgrade head` и `python scripts\seed_products.py` |
| Alembic «ничего не делает» | Миграции уже применены; проверьте `alembic current` |
| `curl` в PowerShell | Используйте `Invoke-RestMethod` или `curl.exe` (см. примеры выше) |

---

## Зависимости

Список в [`requirements.txt`](requirements.txt): FastAPI, Uvicorn, SQLAlchemy, Alembic, pytest, pytest-asyncio, httpx, Faker, email-validator, python-dotenv.
