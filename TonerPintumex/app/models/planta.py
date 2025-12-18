from pydantic import BaseModel
from typing import Optional

class Planta(BaseModel):
    id: Optional[int] = None
    nombrePlanta: str
