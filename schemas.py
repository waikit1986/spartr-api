from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ProfileBase(BaseModel):
    user_name: str
    age: int
    bio: str

class ProfileCreate(ProfileBase):
    id: UUID  # FK to User

class ProfileUpdate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
