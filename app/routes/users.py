from fastapi import APIRouter, HTTPException
from app.models import User
from app.schemas import UserSchema, UserCreateSchema, UserUpdateSchema

router = APIRouter(prefix="/users", tags=["Users"])


# Получить всех пользователей
@router.get("/", response_model=list[UserSchema])
async def get_users():
    return await User.all()


# Создать пользователя
@router.post("/", response_model=UserSchema)
async def create_user(user_data: UserCreateSchema):
    existing_user = await User.get_or_none(login=user_data.login)
    if existing_user:
        raise HTTPException(status_code=400, detail="Login already in use")

    user = await User.create(**user_data.dict())
    return user


# Обновить пользователя по ID
@router.put("/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user_data: UserUpdateSchema):
    user = await User.get_or_none(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user.update_from_dict(user_data.dict(exclude_unset=True))
    await user.save()
    return user


# Удалить пользователя по ID
@router.delete("/{user_id}")
async def delete_user(user_id: int):
    user = await User.get_or_none(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user.delete()
    return {"message": "User deleted successfully"}
