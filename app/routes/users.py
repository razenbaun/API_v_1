from fastapi import APIRouter, HTTPException
from app.models import User
from app.schemas import UserSchema, UserCreateSchema, UserUpdateSchema, AuthRequest
from passlib.context import CryptContext

router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Получить всех пользователей
@router.get("/", response_model=list[UserSchema])
async def get_users():
    return await User.all()


@router.post("/", response_model=UserSchema)
async def create_user(user_data: UserCreateSchema):
    existing_user = await User.get_or_none(login=user_data.login)
    if existing_user:
        raise HTTPException(status_code=400, detail="Login already in use")

    existing_email = await User.get_or_none(email=user_data.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already in use")

    hashed_password = pwd_context.hash(user_data.password)

    user = await User.create(
        email=user_data.email,
        login=user_data.login,
        password=hashed_password,
        admin=user_data.admin
    )

    return user


# Обновить пользователя по ID
@router.put("/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user_data: UserUpdateSchema):
    user = await User.get_or_none(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_data.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = pwd_context.hash(update_data["password"])

    await user.update_from_dict(update_data)
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


# Получить пользователя по ID
@router.get("/{user_id}", response_model=UserSchema)
async def get_user_by_id(user_id: int):
    user = await User.get_or_none(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/auth")
async def authenticate_user(auth_data: AuthRequest):
    user = await User.get_or_none(login=auth_data.login)
    if not user:
        return {"success": False, "message": "Логин не существует"}

    if not pwd_context.verify(auth_data.password, user.password):
        return {"success": False, "message": "Пароль неверный"}

    return {"success": True, "message": "Успех"}


# Получить пользователя по логину
@router.get("/login/{login}", response_model=UserSchema)
async def get_user_by_login(login: str):
    user = await User.get_or_none(login=login)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
