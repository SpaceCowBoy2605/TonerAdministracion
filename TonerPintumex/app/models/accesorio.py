from __future__ import annotations

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

    # Relaciones expandidas (cuando el CRUD haga JOINs)
    estatus: Optional['Estatus'] = None
    factura: Optional['Factura'] = None


# Resolver forward refs (Pydantic v2/v1). Importamos si se puede, sin forzar ciclos.
try:
    from app.models.estatus import Estatus  # noqa: F401
    from app.models.factura import Factura  # noqa: F401
except Exception:
    try:
        from models.estatus import Estatus  # type: ignore  # noqa: F401
        from models.factura import Factura  # type: ignore  # noqa: F401
    except Exception:
        pass

try:
    Accesorio.model_rebuild()
except Exception:
    try:
        Accesorio.update_forward_refs()  # type: ignore[attr-defined]
    except Exception:
        pass