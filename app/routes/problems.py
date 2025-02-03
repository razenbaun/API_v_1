from io import BytesIO

from fastapi import APIRouter, HTTPException, UploadFile, File
from starlette.responses import StreamingResponse

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


async def save_image(img: UploadFile) -> bytes:
    img_data = await img.read()
    return img_data


# Создать проблему
@router.post("/", response_model=ProblemSchema)
async def create_problem(
        computer_id: int,
        user_id: int,
        description: str,
        img: UploadFile = File(None),
        active: bool = True,
        status: str = "Pending",
):
    img_data = None
    if img:
        img_data = await save_image(img)

    problem_data = ProblemCreateSchema(
        description=description,
        img=img_data,
        active=active,
        status=status,
        computer_id=computer_id,
        user_id=user_id
    )

    problem = await Problem.create(**problem_data.dict())
    return problem


# Обновить проблему по ID
@router.put("/{problem_id}", response_model=ProblemUpdateSchema)
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


@router.get("/{problem_id}/image")
async def get_problem_image(problem_id: int):
    problem = await Problem.get_or_none(problem_id=problem_id)
    if not problem or not problem.img:
        raise HTTPException(status_code=404, detail="Image not found")

    image_file = BytesIO(problem.img)
    return StreamingResponse(image_file, media_type="image/jpeg")
