from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Solicitudes(BaseModel):
    id: Optional[int] = None
    idAccesorio: int
    idImpresora: int
    cantidad: int
    fechaSolicitud: datetime
    centroCostos: str 
    idPlanta: int
    idResu: int
    idCedis: int 
    idTep: int