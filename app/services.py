
from app.exceptions import (
    UserNotFoundError,
    InsufficientFundsError,
    InvalidTransferError
)


def transfer_money(
    users: list,
    transactions: list,
    sender_id: int,
    receiver_id: int,
    amount: int
) -> str:

    if amount <= 0:
        raise InvalidTransferError("Некорректная сумма")

    if sender_id == receiver_id:
        raise InvalidTransferError("Перевод самому себе запрещён")

    sender = None
    receiver = None

    for user in users:
        if user["id"] == sender_id:
            sender = user

        if user["id"] == receiver_id:
            receiver = user

    if sender is None or receiver is None:
        raise UserNotFoundError("Пользователь не найден")

    if sender["balance"] < amount:
        raise InsufficientFundsError ("Недостаточно средств")

    sender["balance"] -= amount
    receiver["balance"] += amount
    transactions.append({
      "sender_id": sender['id'],
      "receiver_id": receiver['id'],
      "amount": amount,
      "status": "success"
    })
    return "Перевод успешен"
