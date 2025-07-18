from fastapi import APIRouter, HTTPException
from app.models import Place, Classroom, Device
from app.schemas import PlaceSchema, PlaceCreateSchema, PlaceUpdateSchema, DeviceSchema
from tortoise.transactions import in_transaction

router = APIRouter(prefix="/places", tags=["Places"])


@router.get("/", response_model=list[PlaceSchema])
async def get_places(classroom_id: int = None):
    query = Place.all().prefetch_related("classroom", "devices")
    if classroom_id is not None:
        query = query.filter(classroom_id=classroom_id)
    return await query


@router.get("/{place_id}", response_model=PlaceSchema)
async def get_place(place_id: int):
    place = await Place.get_or_none(place_id=place_id).prefetch_related("classroom", "devices")
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place


@router.post("/", response_model=PlaceSchema)
async def create_place(place_data: PlaceCreateSchema):
    classroom = await Classroom.get_or_none(classroom_id=place_data.classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    existing_place = await Place.filter(
        classroom_id=place_data.classroom_id,
        x=place_data.x,
        y=place_data.y
    ).first()

    if existing_place:
        raise HTTPException(
            status_code=400,
            detail="Place with these coordinates already exists in this classroom"
        )

    place = await Place.create(**place_data.dict())
    return place


@router.put("/{place_id}", response_model=PlaceSchema)
async def update_place(place_id: int, place_data: PlaceUpdateSchema):
    place = await Place.get_or_none(place_id=place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    update_data = place_data.dict(exclude_unset=True)

    if 'x' in update_data or 'y' in update_data:
        x = update_data.get('x', place.x)
        y = update_data.get('y', place.y)

        existing_place = await Place.filter(
            classroom_id=place.classroom_id,
            x=x,
            y=y
        ).exclude(place_id=place_id).first()

        if existing_place:
            raise HTTPException(
                status_code=400,
                detail="Another place with these coordinates already exists in this classroom"
            )

    await place.update_from_dict(update_data)
    await place.save()
    return place


# Удалить место по ID
@router.delete("/{place_id}")
async def delete_place_with_devices(place_id: int):
    async with in_transaction():
        place = await Place.get_or_none(place_id=place_id)
        if not place:
            raise HTTPException(status_code=404, detail="Place not found")

        await Device.filter(place_id=place_id).delete()

        await place.delete()

    return {"message": "Place and all attached devices were deleted successfully"}


# Получить все устройства на месте
@router.get("/{place_id}/devices", response_model=list[DeviceSchema])
async def get_place_devices(place_id: int):
    place = await Place.get_or_none(place_id=place_id).prefetch_related("devices")
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place.devices
