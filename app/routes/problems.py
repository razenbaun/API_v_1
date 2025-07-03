from io import BytesIO
from fastapi import APIRouter, HTTPException, UploadFile, File
from starlette.responses import StreamingResponse
from app.models import Problem, Device
from app.schemas import ProblemSchema, ProblemCreateSchema, ProblemUpdateSchema

router = APIRouter(prefix="/problems", tags=["Problems"])


# Получить все проблемы
@router.get("/", response_model=list[ProblemSchema])
async def get_problems(device_id: int = None, user_id: int = None):
    query = Problem.all().prefetch_related("device", "user")
    if device_id is not None:
        query = query.filter(device_id=device_id)
    if user_id is not None:
        query = query.filter(user_id=user_id)
    return await query


# Получить проблему по ID
@router.get("/{problem_id}", response_model=ProblemSchema)
async def get_problem(problem_id: int):
    problem = await Problem.get_or_none(problem_id=problem_id).prefetch_related("device", "user")
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


async def save_image(img: UploadFile) -> str:
    img_data = await img.read()
    return img_data.decode('latin-1')  # Преобразуем байты в строку для хранения


# Создать проблему
@router.post("/", response_model=ProblemSchema)
async def create_problem(
        device_id: int,
        user_id: int,
        description: str,
        img: UploadFile = File(None),
        active: bool = True,
        status: str = "Pending",
):
    # Проверяем существование устройства
    device = await Device.get_or_none(device_id=device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    img_data = None
    if img:
        img_data = await save_image(img)

    problem_data = ProblemCreateSchema(
        description=description,
        img=img_data,
        active=active,
        status=status,
        device_id=device_id,
        user_id=user_id
    )

    problem = await Problem.create(**problem_data.dict())
    return problem


# Обновить проблему по ID
@router.put("/{problem_id}", response_model=ProblemSchema)
async def update_problem(
        problem_id: int,
        description: str = None,
        active: bool = None,
        status: str = None,
        device_id: int = None,
        user_id: int = None,
        img: UploadFile = File(None)
):
    problem = await Problem.get_or_none(problem_id=problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    if device_id is not None:
        device = await Device.get_or_none(device_id=device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        problem.device_id = device_id

    if img:
        problem.img = await save_image(img)
    if description is not None:
        problem.description = description
    if active is not None:
        problem.active = active
    if status is not None:
        problem.status = status
    if user_id is not None:
        problem.user_id = user_id

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

    # Преобразуем строку обратно в байты
    image_bytes = problem.img.encode('latin-1')
    image_file = BytesIO(image_bytes)
    return StreamingResponse(image_file, media_type="image/jpeg")
