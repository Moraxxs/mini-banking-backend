
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    balance: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        default=0
    )


from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    String,
    func
)
from sqlalchemy.orm import Mapped, mapped_column


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        CheckConstraint("amount > 0"),
        CheckConstraint("sender_id <> receiver_id"),
    )

    id: Mapped[int] = mapped_column(
        Identity(always=True),
        primary_key=True
    )

    sender_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    receiver_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    amount: Mapped[int] = mapped_column(
        BigInteger
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="success"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
