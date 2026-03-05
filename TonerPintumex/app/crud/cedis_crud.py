from typing import Optional

try:
    from app import db
except Exception:
    import db
try:
    from app.models.cedis import Cedis
except Exception:
    from models.cedis import Cedis

def get_cedis_by_id(idCedis: int) -> Optional[Cedis]:
    """Recupera un cedis por id usando la conexión definida en app/db.py.

    Retorna una instancia de `Cedis` o `None` si no existe.
    """
    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idCedis AS id, nombreCedis FROM cedis WHERE idCedis = %s",
            (idCedis,)
        )
        row = cur.fetchone()
    finally:
        cur.close()

    if not row:
        return None

    return Cedis(**row)

def get_all_cedis() -> list[Cedis]:
    """Recupera todos los cedis usando la conexión definida en app/db.py.

    Retorna una lista de instancias de `Cedis`.
    """
    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idCedis AS id, nombreCedis FROM cedis"
        )
        rows = cur.fetchall()
    finally:
        cur.close()

    return [Cedis(**row) for row in rows]