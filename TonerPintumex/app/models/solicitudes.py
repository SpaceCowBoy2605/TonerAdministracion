from __future__ import annotations

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Solicitudes(BaseModel):
    id: Optional[int] = None

    # FKs
    idAccesorio: Optional[int] = None
    idImpresora: Optional[int] = None

    cantidad: int
    fechaSolicitud: datetime
    centroCostos: Optional[str] = None

    idPlanta: Optional[int] = None
    idResu: Optional[int] = None
    idCedis: Optional[int] = None
    idTep: Optional[int] = None

    # Objetos anidados (cuando el CRUD haga JOINs)
    accesorio: Optional['Accesorio'] = None
    impresora: Optional['Impresora'] = None
    planta: Optional['Planta'] = None
    resu: Optional['Resurrecion'] = None
    cedis: Optional['Cedis'] = None
    tep: Optional['Tep'] = None


# Resolver forward refs (Pydantic v2/v1). Importamos si se puede, sin forzar ciclos.
try:
    from app.models.accesorio import Accesorio  # noqa: F401
    from app.models.impresora import Impresora  # noqa: F401
    from app.models.planta import Planta  # noqa: F401
    from app.models.resu import Resurrecion  # noqa: F401
    from app.models.cedis import Cedis  # noqa: F401
    from app.models.tep import Tep  # noqa: F401
except Exception:
    try:
        from app.models.accesorio import Accesorio  # type: ignore  # noqa: F401
        from app.models.impresora import Impresora  # type: ignore  # noqa: F401
        from app.models.planta import Planta  # type: ignore  # noqa: F401
        from app.models.resu import Resurrecion  # type: ignore  # noqa: F401
        from app.models.cedis import Cedis  # type: ignore  # noqa: F401
        from app.models.tep import Tep  # type: ignore  # noqa: F401
    except Exception:
        pass

try:
    Solicitudes.model_rebuild()
except Exception:
    try:
        Solicitudes.update_forward_refs()  # type: ignore[attr-defined]
    except Exception:
        pass