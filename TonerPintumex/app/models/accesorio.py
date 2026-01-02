from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Accesorio(BaseModel):
    id: Optional[int] = None
    nombreAccesorio: str
    cantidad : int
    idEstatus: int
    entrada: datetime
    idfactura: Optional[int] = None