from pydantic import BaseModel, Field
from enum import Enum
from typing import List
import uuid
from uuid import UUID

class Gender(str, Enum):
    male = "male"
    female = "female"
    nonbinary = "nonbinary"

class Role(str, Enum):
    admin = "admin"
    user = "user"
    student = "student"
    
class User(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4) 
    name: str
    gender: Gender
    roles: List[Role]
    email : str
    password : str

class UserUpdate(BaseModel):
    name : str | None = None 
    gender : Gender | None = None
    roles : List[Role] | None = None
    email : str | None = None
    password : str | None = None
