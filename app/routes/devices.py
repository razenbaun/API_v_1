from fastapi import APIRouter, HTTPException
from app.models import Device, Place
from app.schemas import DeviceSchema, DeviceCreateSchema, DeviceUpdateSchema

router = APIRouter(prefix="/devices", tags=["Devices"])


# Получить все устройства
@router.get("/", response_model=list[DeviceSchema])
async def get_devices():
    return await Device.all().prefetch_related("place", "problems")


# Получить устройство по ID
@router.get("/{device_id}", response_model=DeviceSchema)
async def get_device_by_id(device_id: int):
    device = await Device.get_or_none(device_id=device_id).prefetch_related("place", "problems")
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


# Создать устройство
@router.post("/", response_model=DeviceSchema)
async def create_device(device_data: DeviceCreateSchema):
    # Проверяем существование места
    place = await Place.get_or_none(place_id=device_data.place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    device = await Device.create(**device_data.dict())
    return device


# Обновить устройство по ID
@router.put("/{device_id}", response_model=DeviceSchema)
async def update_device(device_id: int, device_data: DeviceUpdateSchema):
    device = await Device.get_or_none(device_id=device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Если обновляется place_id, проверяем существование нового места
    if device_data.place_id is not None:
        place = await Place.get_or_none(place_id=device_data.place_id)
        if not place:
            raise HTTPException(status_code=404, detail="New place not found")

    await device.update_from_dict(device_data.dict(exclude_unset=True))
    await device.save()
    return device


# Удалить устройство по ID
@router.delete("/{device_id}")
async def delete_device(device_id: int):
    device = await Device.get_or_none(device_id=device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    await device.delete()
    return {"message": "Device deleted successfully"}


# Получить все устройства в конкретном месте
@router.get("/place/{place_id}", response_model=list[DeviceSchema])
async def get_devices_by_place(place_id: int):
    place = await Place.get_or_none(place_id=place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    devices = await place.devices.all().prefetch_related("problems")
    return devices
