from pydantic import BaseModel
from typing import Optional
from datetime import date

class Factura(BaseModel):
    id: Optional[int] = None
    fecha: date