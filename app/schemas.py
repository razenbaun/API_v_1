from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CampusSchema(BaseModel):
    campus_id: int
    campus_number: int
    address: str

    class Config:
        from_attributes = True


class CampusCreateSchema(BaseModel):
    campus_number: int
    address: str


class CampusUpdateSchema(BaseModel):
    campus_number: Optional[int] = None
    address: Optional[str] = None


class ClassroomSchema(BaseModel):
    classroom_id: int
    classroom_number: int
    campus_id: int

    class Config:
        from_attributes = True


class ClassroomCreateSchema(BaseModel):
    classroom_number: int
    campus_id: int


class ClassroomUpdateSchema(BaseModel):
    classroom_number: Optional[int] = None
    campus_id: Optional[int] = None


class PlaceSchema(BaseModel):
    place_id: int
    x: int
    y: int
    placeType: str
    classroom_id: int

    class Config:
        from_attributes = True


class PlaceCreateSchema(BaseModel):
    x: int
    y: int
    placeType: str = "standard"
    classroom_id: int


class PlaceUpdateSchema(BaseModel):
    x: Optional[int] = None
    y: Optional[int] = None
    placeType: Optional[str] = None
    classroom_id: Optional[int] = None


class DeviceSchema(BaseModel):
    device_id: int
    place_id: int
    status: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class DeviceCreateSchema(BaseModel):
    place_id: int
    description: Optional[str] = None


class DeviceUpdateSchema(BaseModel):
    place_id: Optional[int] = None
    status: Optional[str] = None
    description: Optional[str] = None


class UserSchema(BaseModel):
    user_id: int
    email: str
    login: str
    admin: bool
    password: str

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    email: str
    login: str
    password: str
    admin: Optional[bool] = False


class UserUpdateSchema(BaseModel):
    email: str
    login: Optional[str] = None
    password: Optional[str] = None
    admin: Optional[bool] = None


class AuthRequest(BaseModel):
    login: str
    password: str


class ProblemSchema(BaseModel):
    problem_id: int
    description: str
    active: bool
    status: str
    device_id: int
    user_id: int
    img: Optional[bytes] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            bytes: lambda v: v.decode('latin-1') if v else None
        }


class ProblemCreateSchema(BaseModel):
    description: str
    img: Optional[bytes] = None
    active: bool = True
    status: str = Field("Pending", pattern="^(Pending|In Progress|Resolved)$")
    device_id: int
    user_id: int

    class Config:
        json_encoders = {
            bytes: lambda v: v.decode('latin-1') if v else None
        }


class ProblemUpdateSchema(BaseModel):
    description: Optional[str] = None
    img: Optional[bytes] = None
    active: Optional[bool] = None
    status: Optional[str] = Field(None, pattern="^(Pending|In Progress|Resolved)$")
    device_id: Optional[int] = None
    user_id: Optional[int] = None

    class Config:
        json_encoders = {
            bytes: lambda v: v.decode('latin-1') if v else None
        }
