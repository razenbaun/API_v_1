from pydantic import BaseModel
from typing import Optional


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


class ComputerSchema(BaseModel):
    computer_id: int
    computer_ip: str
    classroom_id: int
    status: str

    class Config:
        from_attributes = True


class ComputerCreateSchema(BaseModel):
    computer_ip: str
    classroom_id: int


class ComputerUpdateSchema(BaseModel):
    computer_ip: Optional[str] = None
    classroom_id: Optional[int] = None


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


class ProblemSchema(BaseModel):
    problem_id: int
    description: str
    active: bool
    status: str
    computer_id: int
    user_id: int

    class Config:
        from_attributes = True


class ProblemCreateSchema(BaseModel):
    description: str
    img: Optional[bytes] = None
    active: bool = True
    status: str = "Pending"
    computer_id: int
    user_id: int


class ProblemUpdateSchema(BaseModel):
    description: Optional[str] = None
    img: Optional[bytes] = None
    active: Optional[bool] = None
    status: Optional[str] = None
    computer_id: Optional[int] = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
