from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.error_handlers import register_exception_handlers
from app.exceptions import CustomExceptionA, CustomExceptionB
from app.models import Product
from app.schemas.errors import ErrorResponse, ValidationErrorResponse
from app.routers import records as records_router
from app.schemas.user import User

app = FastAPI(
    title="Products API",
    responses={
        400: {"model": ErrorResponse, "description": "Business rule violation"},
        404: {"model": ErrorResponse, "description": "Resource not found"},
        422: {"model": ValidationErrorResponse, "description": "Validation failed"},
    },
)

register_exception_handlers(app)
app.include_router(records_router.router)


@app.get("/products")
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.get(
    "/products/{product_id}",
    responses={404: {"model": ErrorResponse}},
)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise CustomExceptionB(
            message=f"Product with id={product_id} was not found",
        )
    return product


@app.get(
    "/products/{product_id}/reserve",
    responses={400: {"model": ErrorResponse}},
)
def reserve_product(
    product_id: int,
    quantity: int = Query(..., ge=1, description="Units to reserve"),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise CustomExceptionB(
            message=f"Product with id={product_id} was not found",
        )
    if product.count < quantity:
        raise CustomExceptionA(
            message=(
                f"Not enough stock for product id={product_id}: "
                f"requested {quantity}, available {product.count}"
            ),
        )
    return {
        "product_id": product_id,
        "reserved": quantity,
        "remaining": product.count - quantity,
    }


@app.post(
    "/users/register",
    status_code=201,
    responses={422: {"model": ValidationErrorResponse}},
)
def register_user(user: User):
    return {
        "username": user.username,
        "age": user.age,
        "email": str(user.email),
        "phone": user.phone,
    }


@app.get("/health")
def health():
    return {"status": "ok"}
