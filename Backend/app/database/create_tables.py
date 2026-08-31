from app.database.database import Base, engine
from app.database import db_models


def create_tables():

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "MangoCare MySQL tables created successfully."
    )


if __name__ == "__main__":
    create_tables()