from fastapi import APIRouter, HTTPException
from app.models import Computer
from app.schemas import ComputerSchema, ComputerCreateSchema, ComputerUpdateSchema

router = APIRouter(prefix="/computers", tags=["Computers"])


# Получить все компьютеры
@router.get("/", response_model=list[ComputerSchema])
async def get_computers():
    return await Computer.all()


# Создать компьютер
@router.post("/", response_model=ComputerSchema)
async def create_computer(computer_data: ComputerCreateSchema):
    computer = await Computer.create(**computer_data.dict())
    return computer


# Обновить компьютер по ID
@router.put("/{computer_id}", response_model=ComputerSchema)
async def update_computer(computer_id: int, computer_data: ComputerUpdateSchema):
    computer = await Computer.get_or_none(computer_id=computer_id)
    if not computer:
        raise HTTPException(status_code=404, detail="Computer not found")

    await computer.update_from_dict(computer_data.dict(exclude_unset=True))
    await computer.save()
    return computer


# Удалить компьютер по ID
@router.delete("/{computer_id}")
async def delete_computer(computer_id: int):
    computer = await Computer.get_or_none(computer_id=computer_id)
    if not computer:
        raise HTTPException(status_code=404, detail="Computer not found")

    await computer.delete()
    return {"message": "Computer deleted successfully"}
