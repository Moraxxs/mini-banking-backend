from sqlalchemy import create_engine, text

DATABASE_URL = (
    "postgresql+psycopg:///"
    "mini_banking"
)

engine = create_engine(DATABASE_URL)
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False
)

def check_connection():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT version();")
        )
        print(result.scalar())


def get_all_users():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM users ORDER BY id")
        )
        return [
            dict(row)
            for row in result.mappings()
        ]


def get_user_by_id(user_id: int):
    with engine.connect() as connection:
        result = connection.execute(
            text(
                "SELECT * FROM users WHERE id = :user_id"
            ),
            {"user_id": user_id}
        )
        user = result.mappings().first()

        if user is None:
            return None

        return dict(user)



def delete_user_by_id(user_id: int):
    with engine.begin() as connection:
        result = connection.execute(
            text("DELETE FROM users WHERE id = :user_id"),
            {"user_id": user_id}
        )
        if result.rowcount == 0:
            return False
        return True


def create_user_db(name: str, balance: int):
    with engine.begin() as connection:
        result = connection.execute(
            text("""
                INSERT INTO users (name, balance)
                VALUES (:name, :balance)
                RETURNING id, name, balance
            """),
            {
                "name": name,
                "balance": balance
            }
        )
        new_user = result.mappings().one()
        return dict(new_user)


def update_user_db(
    user_id: int,
    name: str,
    balance: int
):
    with engine.begin() as connection:
        result = connection.execute(
            text("""
                UPDATE users
                SET name = :name,
                    balance = :balance
                WHERE id = :user_id
                RETURNING id, name, balance
            """),
            {
                "user_id": user_id,
                "name": name,
                "balance": balance
            }
        )

        updated_user = result.mappings().first()

        if updated_user is None:
            return None
        return dict(updated_user)


    
