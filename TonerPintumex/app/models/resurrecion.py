from pydantic import BaseModel
from typing import Optional

class Resurrecion(BaseModel):
    idResu: Optional[int] = None
    nombreResu: str