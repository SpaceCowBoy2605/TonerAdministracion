from pydantic import BaseModel
from typing import Optional

class Estatus(BaseModel):
    id: Optional[int] = None
    estatus: str