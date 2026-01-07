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
    idPlanta: Optional[int] = None
    idResu: Optional[int] = None
    idCedis: Optional[int] = None 
    idTep: Optional[int] = None