import os
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
from tortoise.exceptions import DBConnectionError, OperationalError

DB_URL = os.getenv("DATABASE_URL", "").replace("postgresql://", "postgres://")

if not DB_URL:
    raise ValueError("DATABASE_URL is not set in environment variables!")


async def init_db():
    try:
        await Tortoise.init(
            db_url=DB_URL,
            modules={"models": ["app.models"]},
            _create_db=True
        )
        await Tortoise.generate_schemas(safe=True)
        print("Database initialized successfully")
    except (DBConnectionError, OperationalError) as e:
        print(f"Failed to initialize database: {str(e)}")
        raise


def register_db(app: FastAPI):
    register_tortoise(
        app,
        db_url=DB_URL,
        modules={"models": ["app.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
