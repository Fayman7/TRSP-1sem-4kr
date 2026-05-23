from fastapi import APIRouter, HTTPException, Response

from app import users_store
from app.schemas.user_memory import UserIn, UserOut

router = APIRouter(tags=["users-memory"])


@router.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserIn) -> UserOut:
    row = users_store.create(username=user.username, age=user.age)
    return UserOut(**row)


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int) -> UserOut:
    row = users_store.get(user_id)
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**row)


@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int) -> Response:
    if not users_store.delete(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)
