from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HistorialAccesorios(BaseModel):
    id: Optional[int] = None
    idfactura: int
    idAccesorio: int
    fecha: datetime
    cantidad: int