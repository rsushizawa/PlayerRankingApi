from pydantic import BaseModel, Field
from typing import Optional

class Player(BaseModel):
    id: int
    name: str
    points: int = Field(gt=0, datail="Field must be positive")

class UpdatePlayer(BaseModel):
    name: Optional[str]
    points: Optional[int] = Field(gt=0, datail="Field must be positive")
