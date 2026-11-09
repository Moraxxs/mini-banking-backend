
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.models import users
from app.models import users, transactions
from app.services import transfer_money
from app.exceptions import (
    UserNotFoundError,
    InsufficientFundsError,
    InvalidTransferError
)



from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from app.database import (
    get_all_users,
    get_user_by_id,
    delete_user_by_id,
    create_user_db,
    update_user_db,
)

app = FastAPI()


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    balance: int = Field(ge=0)


@app.get("/users")
def get_users():
    return get_all_users()


@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    deleted = delete_user_by_id(user_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )
    return {
        "message": "Пользователь удалён"
    }

@app.post("/users", status_code=201)
def create_user(data: UserCreate):
    new_user = create_user_db(
        name=data.name,
        balance=data.balance
    )
    return new_user


@app.put("/users/{user_id}")
def update_user(user_id: int, data: UserCreate):
    user = update_user_db(
        user_id=user_id,
        name=data.name,
        balance=data.balance
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )

    return user


from app.orm_services import (
    get_all_users_orm, 
    get_user_by_id_orm,
    update_user_orm
)

@app.get("/orm/users")
def get_orm_users():
    return get_all_users_orm()

print (get_user_by_id_orm(1))

@app.put("/users/{user_id}")
def update_user(user_id: int, data: UserCreate):

    updated_user = update_user_orm(
        user_id=user_id,
        name=data.name,
        balance=data.balance
    )

    if updated_user is None:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )

    return updated_user