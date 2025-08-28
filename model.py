from pydantic import BaseModel, Field
from typing import Optional

class Player(BaseModel):
    id: int
    name: str
    points: int = Field(gt=0, detail="Field must be positive")

class CreatePlayer(BaseModel):
    name: str
    points: int = Field(gt=0, detail="Field must be positive") 

class UpdatePlayer(BaseModel):
    name: Optional[str] = None
    points: Optional[int] = Field(gt=0, detail="Field must be positive")
