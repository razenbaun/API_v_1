from fastapi import APIRouter, HTTPException
from app.models import Campus
from app.schemas import CampusSchema, CampusCreateSchema, CampusUpdateSchema, ClassroomSchema  # импортируем ClassroomSchema
from app.models import Classroom

router = APIRouter(prefix="/campus", tags=["Campus"])


# Получить все кампусы
@router.get("/", response_model=list[CampusSchema])
async def get_campuses():
    return await Campus.all()


# # Получить кампус по ID
# @router.get("/{campus_id}", response_model=CampusSchema)
# async def get_campus(campus_id: int):
#     campus = await Campus.get_or_none(campus_id=campus_id)
#     if not campus:
#         raise HTTPException(status_code=404, detail="Campus not found")
#     return campus


# Создать кампус
@router.post("/", response_model=CampusSchema)
async def create_campus(campus_data: CampusCreateSchema):
    campus = await Campus.create(**campus_data.dict())
    return campus


# Обновить кампус по ID
@router.put("/{campus_id}", response_model=CampusSchema)
async def update_campus(campus_id: int, campus_data: CampusUpdateSchema):
    campus = await Campus.get_or_none(campus_id=campus_id)
    if not campus:
        raise HTTPException(status_code=404, detail="Campus not found")

    await campus.update_from_dict(campus_data.dict(exclude_unset=True))
    await campus.save()
    return campus


# Удалить кампус по ID
@router.delete("/{campus_id}")
async def delete_campus(campus_id: int):
    campus = await Campus.get_or_none(campus_id=campus_id)
    if not campus:
        raise HTTPException(status_code=404, detail="Campus not found")

    await campus.delete()
    return {"message": "Campus deleted successfully"}


# Получить все аудитории, принадлежащие кампусу по ID
@router.get("/{campus_id}/classrooms", response_model=list[ClassroomSchema])
async def get_classrooms_by_campus(campus_id: int):
    campus = await Campus.get_or_none(campus_id=campus_id)
    if not campus:
        raise HTTPException(status_code=404, detail="Campus not found")

    classrooms = await campus.classrooms.all()
    return classrooms
