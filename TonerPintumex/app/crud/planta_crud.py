from typing import Optional

# Fallback imports: funcionan si ejecutas desde la raíz (package `app`) o
# si ejecutas el script desde la carpeta `app` (CWD = app).
try:
    from app import db
except Exception:
    import db

try:
    from app.models.planta import Planta
except Exception:
    from models.planta import Planta


def get_planta_by_id(idPlanta: int) -> Optional[Planta]:
    """Recupera una planta por id usando la conexión definida en app/db.py.

    Retorna una instancia de `Planta` o `None` si no existe.
    """
    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idPlanta AS id, nombrePlanta FROM Planta WHERE idPlanta = %s",
            (idPlanta,)
        )
        row = cur.fetchone()
    finally:
        cur.close()

    if not row:
        return None

    return Planta(**row)