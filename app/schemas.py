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


from pydantic import BaseModel
from typing import Optional


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
