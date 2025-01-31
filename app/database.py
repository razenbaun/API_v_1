from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI

DB_URL = "sqlite://db.sqlite3"


async def init_db():
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models": ["app.models"]}
    )
    await Tortoise.generate_schemas()


def register_db(app: FastAPI):
    register_tortoise(
        app,
        db_url=DB_URL,
        modules={"models": ["app.models"]},
        generate_schemas=True,
        add_exception_handlers=True
    )
