# FastAPI + Alembic (SQLite)

Учебный проект: миграции схемы БД для сущности `Product` (FastAPI, SQLAlchemy 2, Alembic, SQLite).

## Структура

```
fastapi-alembic-products/
├── app/
│   ├── database.py
│   ├── models.py
│   ├── exceptions.py      # CustomExceptionA, CustomExceptionB
│   ├── error_handlers.py  # регистрация обработчиков
│   ├── schemas/errors.py  # Pydantic ErrorResponse
│   └── main.py
├── alembic/           # env.py, versions/
├── scripts/
│   ├── seed_products.py
│   ├── verify_db.py
│   └── test_error_handling.py
├── alembic.ini
└── requirements.txt
```

## Установка

```powershell
cd fastapi-alembic-products
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
```

## Миграции

**1. Начальная таблица `products` (id, title, price, count):**

```powershell
.\.venv\Scripts\alembic revision --autogenerate -m "create products table"
.\.venv\Scripts\alembic upgrade head
.\.venv\Scripts\python scripts\seed_products.py   # после первой миграции — без description в модели
```

**2. Поле `description` (NOT NULL):**

После добавления поля в `app/models.py`:

```powershell
.\.venv\Scripts\alembic revision --autogenerate -m "add product description"
.\.venv\Scripts\alembic upgrade head
.\.venv\Scripts\python scripts\verify_db.py
```

## Проверка

```powershell
.\.venv\Scripts\python scripts\verify_db.py
```

Ожидаемые колонки: `id`, `title`, `price`, `count`, `description`.

## Запуск API

```powershell
.\.venv\Scripts\uvicorn app.main:app --reload
```

Откройте http://127.0.0.1:8000/docs

## Обработка ошибок

| Исключение | HTTP | `error_code` | Когда |
|------------|------|--------------|--------|
| `CustomExceptionA` | 400 | `condition_not_met` | Недостаточно товара на складе |
| `CustomExceptionB` | 404 | `resource_not_found` | Товар не найден |

**Эндпоинты для проверки:**

- `GET /products/9999` → 404, `CustomExceptionB`
- `GET /products/1/reserve?quantity=1000` → 400, `CustomExceptionA` (если на складе меньше 1000)

Формат ответа (Pydantic `ErrorResponse`):

```json
{
  "error_code": "resource_not_found",
  "message": "Product with id=9999 was not found",
  "status_code": 404
}
```

**Автотест:**

```powershell
.\.venv\Scripts\python scripts\test_error_handling.py
```

**Ручная проверка** (сервер должен быть запущен):

```powershell
curl http://127.0.0.1:8000/products/9999
curl "http://127.0.0.1:8000/products/1/reserve?quantity=1000"
```

В консоли сервера появятся строки `[ERROR] ...` (простое логирование через `print`).
