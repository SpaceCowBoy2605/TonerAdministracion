from pydantic import BaseModel
from typing import Optional

class Cedis(BaseModel):
    id: Optional[int] = None
    nombreCedis: str