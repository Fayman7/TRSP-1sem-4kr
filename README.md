# FastAPI + Alembic (SQLite)

Учебный проект: миграции схемы БД для сущности `Product` (FastAPI, SQLAlchemy 2, Alembic, SQLite).

## Структура

```
fastapi-alembic-products/
├── app/
│   ├── database.py    # engine, SessionLocal, Base
│   ├── models.py      # Product
│   └── main.py        # FastAPI
├── alembic/           # env.py, versions/
├── scripts/
│   ├── seed_products.py
│   └── verify_db.py
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
