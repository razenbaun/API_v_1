from fastapi import APIRouter, HTTPException
from app.models import Problem
from app.schemas import ProblemSchema, ProblemCreateSchema, ProblemUpdateSchema

router = APIRouter(prefix="/problems", tags=["Problems"])


# Получить все проблемы
@router.get("/", response_model=list[ProblemSchema])
async def get_problems():
    return await Problem.all()


# Получить проблему по ID
@router.get("/{problem_id}", response_model=ProblemSchema)
async def get_problem(problem_id: int):
    problem = await Problem.get_or_none(problem_id=problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


# Создать проблему
@router.post("/", response_model=ProblemSchema)
async def create_problem(problem_data: ProblemCreateSchema):
    problem = await Problem.create(**problem_data.dict())
    return problem


# Обновить проблему по ID
@router.put("/{problem_id}", response_model=ProblemSchema)
async def update_problem(problem_id: int, problem_data: ProblemUpdateSchema):
    problem = await Problem.get_or_none(problem_id=problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    await problem.update_from_dict(problem_data.dict(exclude_unset=True))
    await problem.save()
    return problem


# Удалить проблему по ID
@router.delete("/{problem_id}")
async def delete_problem(problem_id: int):
    problem = await Problem.get_or_none(problem_id=problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    await problem.delete()
    return {"message": "Problem deleted successfully"}
