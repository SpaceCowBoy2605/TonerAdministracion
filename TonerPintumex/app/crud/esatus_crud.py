from typing import Optional

try:
    from app import db
except Exception:
    import db

try:
    from app.models.estatus import Estatus
except Exception:
    from models.estatus import Estatus  

def get_estatus_by_id(idEstatus: int) -> Optional[Estatus]:
    """Recupera un estatus por id usando la conexión definida en app/db.py.

    Retorna una instancia de `Estatus` o `None` si no existe.
    """
    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idEstatus AS id, estatus FROM estatus WHERE idEstatus = %s",
            (idEstatus,)
        )
        row = cur.fetchone()
    finally:
        cur.close()

    if not row:
        return None

    return Estatus(**row)

def get_all_estatus() -> Optional[Estatus]:
    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idEstatus AS id, estatus FROM estatus"
        )
        rows = cur.fetchall()
    finally:
        cur.close()

    if not rows:
        return None

    estatus_list = [Estatus(**row) for row in rows]
    return estatus_list