from fastapi import FastAPI
from app.database import init_db
from app.routes import campus, classrooms, computers, users, problems

app = FastAPI(title="Campus Management API")


# uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload


@app.on_event("startup")
async def startup():
    await init_db()


app.include_router(campus.router)
app.include_router(classrooms.router)
# app.include_router(computers.router)
# app.include_router(users.router)
# app.include_router(problems.router)


@app.get("/")
async def root():
    return {"message": "API is running!"}
