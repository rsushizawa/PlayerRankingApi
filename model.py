from pydantic import BaseModel, Field
from typing import Optional

class Player(BaseModel):
    id: int
    name: str
    points: int = Field(gt=0)

class CreatePlayer(BaseModel):
    name: str
    points: int = Field(gt=0) 

class UpdatePlayer(BaseModel):
    name: Optional[str] = None
    points: Optional[int] = Field(default=None, gt=0)
