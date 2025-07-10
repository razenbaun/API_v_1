from io import BytesIO
from fastapi import APIRouter, HTTPException, UploadFile, File
from starlette.responses import StreamingResponse
from app.models import Problem, Device
from app.schemas import ProblemSchema, ProblemCreateSchema, ProblemUpdateSchema

router = APIRouter(prefix="/problems", tags=["Problems"])


@router.get("/", response_model=list[ProblemSchema])
async def get_problems(device_id: int = None, user_id: int = None):
    query = Problem.all().prefetch_related("device", "user")
    if device_id is not None:
        query = query.filter(device_id=device_id)
    if user_id is not None:
        query = query.filter(user_id=user_id)
    return await query


@router.get("/{problem_id}", response_model=ProblemSchema)
async def get_problem(problem_id: int):
    problem = await Problem.get_or_none(problem_id=problem_id).prefetch_related("device", "user")
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


@router.post("/", response_model=ProblemSchema)
async def create_problem(
    problem_data: ProblemCreateSchema
):
    device = await Device.get_or_none(device_id=problem_data.device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    problem = await Problem.create(
        description=problem_data.description,
        active=problem_data.active,
        status=problem_data.status,
        device_id=problem_data.device_id,
        user_id=problem_data.user_id
    )
    return problem


@router.put("/{problem_id}", response_model=ProblemSchema)
async def update_problem(
        problem_id: int,
        problem_data: ProblemUpdateSchema
):
    problem = await Problem.get_or_none(problem_id=problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    update_data = problem_data.dict(exclude_unset=True)

    if 'device_id' in update_data:
        device = await Device.get_or_none(device_id=update_data['device_id'])
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")

    await problem.update_from_dict(update_data)
    await problem.save()
    return problem


@router.delete("/{problem_id}")
async def delete_problem(problem_id: int):
    problem = await Problem.get_or_none(problem_id=problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    await problem.delete()
    return {"message": "Problem deleted successfully"}
