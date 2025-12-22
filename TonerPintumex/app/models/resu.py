from pydantic import BaseModel
from typing import Optional

class Resurrecion(BaseModel):
    id: Optional[int] = None
    nombreResu: str