from typing import Optional

try:
    from app import db
except Exception:
    import db

try:
    from app.models.accesorio import Accesorio
except Exception:
    from models.accesorio import Accesorio

def get_accesorio_by_id(idAccesorio: int) -> Optional[Accesorio]:

    """Recupera un accesorio por id usando la conexión definida en app/db.py.

    Retorna una instancia de `Accesorio` o `None` si no existe.
    """
    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idAccesorio AS id, nombreAccesorio, cantidad, status, entrada FROM accesorio WHERE idAccesorio = %s",
            (idAccesorio,)
        )
        row = cur.fetchone()
    finally:
        cur.close()

    if not row:
        return None

    return Accesorio(**row)
