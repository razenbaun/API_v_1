from fastapi import APIRouter, HTTPException
from app.models import Classroom, Place, Device
from app.schemas import (
    ClassroomSchema,
    ClassroomCreateSchema,
    ClassroomUpdateSchema,
    PlaceSchema,
    DeviceSchema
)

router = APIRouter(prefix="/classrooms", tags=["Classrooms"])


# Получить все аудитории
@router.get("/", response_model=list[ClassroomSchema])
async def get_classrooms():
    return await Classroom.all()


# Создать аудиторию
@router.post("/", response_model=ClassroomSchema)
async def create_classroom(classroom_data: ClassroomCreateSchema):
    classroom = await Classroom.create(**classroom_data.dict())
    return classroom


# Обновить аудиторию по ID
@router.put("/{classroom_id}", response_model=ClassroomSchema)
async def update_classroom(classroom_id: int, classroom_data: ClassroomUpdateSchema):
    classroom = await Classroom.get_or_none(classroom_id=classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    await classroom.update_from_dict(classroom_data.dict(exclude_unset=True))
    await classroom.save()
    return classroom


# Удалить аудиторию по ID
@router.delete("/{classroom_id}")
async def delete_classroom(classroom_id: int):
    classroom = await Classroom.get_or_none(classroom_id=classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    await classroom.delete()
    return {"message": "Classroom deleted successfully"}


# Получить все места в аудитории по ID
@router.get("/{classroom_id}/places", response_model=list[PlaceSchema])
async def get_places_by_classroom(classroom_id: int):
    classroom = await Classroom.get_or_none(classroom_id=classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    places = await classroom.places.all()
    return places


# Получить все устройства в аудитории по ID
@router.get("/{classroom_id}/devices", response_model=list[DeviceSchema])
async def get_devices_by_classroom(classroom_id: int):
    classroom = await Classroom.get_or_none(classroom_id=classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    # Получаем все места в аудитории и устройства в них
    places = await classroom.places.all()
    devices = []
    for place in places:
        place_devices = await place.devices.all()
        devices.extend(place_devices)

    return devices
