from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product

app = FastAPI(title="Products API")


@app.get("/products")
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.get("/health")
def health():
    return {"status": "ok"}
