from pydantic import BaseModel
from typing import Optional

class Impresora(BaseModel):
    id: Optional[int] = None
    nombreImpresora: str
    modelo: str
    idAccesorio: Optional[int] = None
    idCedis: Optional[int] = None
    idPlanta: Optional[int] = None
    idResu: Optional[int] = None
    idTep: Optional[int] = None
