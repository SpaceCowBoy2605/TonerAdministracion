from __future__ import annotations

from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING
import importlib


if TYPE_CHECKING:
    from app.models.accesorio import Accesorio
    from app.models.cedis import Cedis
    from app.models.planta import Planta
    from app.models.resu import Resurrecion
    from app.models.tep import Tep


class Impresora(BaseModel):
    id: Optional[int] = None
    nombreImpresora: str
    modelo: str

    # FKs (se siguen devolviendo para compatibilidad)
    idAccesorio: Optional[int] = None
    idCedis: Optional[int] = None
    idPlanta: Optional[int] = None
    idResu: Optional[int] = None
    idTep: Optional[int] = None

    # Objetos anidados (cuando el CRUD haga JOINs)
    accesorio: Optional['Accesorio'] = None
    cedis: Optional['Cedis'] = None
    planta: Optional['Planta'] = None
    resu: Optional['Resurrecion'] = None
    tep: Optional['Tep'] = None

def _try_import_class(module_name: str, class_name: str):
    try:
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    except Exception:
        return None


_types_ns: dict[str, object] = {}
for mod, cls in (
    ("app.models.accesorio", "Accesorio"),
    ("app.models.cedis", "Cedis"),
    ("app.models.planta", "Planta"),
    ("app.models.resu", "Resurrecion"),
    ("app.models.tep", "Tep"),
    ("models.accesorio", "Accesorio"),
    ("models.cedis", "Cedis"),
    ("models.planta", "Planta"),
    ("models.resu", "Resurrecion"),
    ("models.tep", "Tep"),
):
    obj = _try_import_class(mod, cls)
    if obj is not None:
        _types_ns[cls] = obj

try:
    Impresora.model_rebuild(_types_namespace=_types_ns, raise_errors=False)
except Exception:
    try:
        Impresora.update_forward_refs(**_types_ns)  # type: ignore[attr-defined]
    except Exception:
        pass