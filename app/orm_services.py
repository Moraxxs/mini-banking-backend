
from sqlalchemy import select

from app.database import SessionLocal
from app.orm_models import User, Transaction


def get_all_users_orm():
    with SessionLocal() as session:
        statement = select(User)

        users = session.scalars(statement).all()

        return [
            {
                "id": user.id,
                "name": user.name,
                "balance": user.balance
            }
            for user in users
        ]
    
def get_user_by_id_orm(user_id: int):
    with SessionLocal() as session:
        user = session.get(User, user_id)

        if user is None: 
            return None
        return user

def update_user_orm(
    user_id: int,
    name: str,
    balance: int
):
    with SessionLocal() as session:

        # 1. Ищем пользователя
        user = session.get(User, user_id)

        # 2. Проверяем существование
        if user is None:
            return None

        # 3. Изменяем данные
        user.name = name
        user.balance = balance

        # 4. Сохраняем изменения
        session.commit()

        # 5. Обновляем объект из БД
        session.refresh(user)

        # 6. Возвращаем данные
        return {
            "id": user.id,
            "name": user.name,
            "balance": user.balance
        }



from app.exceptions import (
    UserNotFoundError,
    InsufficientFundsError,
    InvalidTransferError
)


def transfer_money_orm(
    sender_id: int,
    receiver_id: int,
    amount: int
) -> str:

    if amount <= 0:
        raise InvalidTransferError("Некорректная сумма")

    if sender_id == receiver_id:
        raise InvalidTransferError(
            "Перевод самому себе запрещён"
        )

    with SessionLocal() as session:
        try:
            sender = session.get(User, sender_id)
            receiver = session.get(User, receiver_id)

            if sender is None or receiver is None:
                raise UserNotFoundError(
                    "Пользователь не найден"
                )

            if sender.balance < amount:
                raise InsufficientFundsError(
                    "Недостаточно средств"
                )

            sender.balance -= amount
            receiver.balance += amount

            transaction = Transaction(
                sender_id=sender_id,
                receiver_id=receiver_id,
                amount=amount,
                status="success"
            )
            session.add(transaction)

            session.commit()

            return "Перевод успешен"

        except Exception:
            session.rollback()
            raise
