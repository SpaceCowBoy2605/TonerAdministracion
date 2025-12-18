from typing import Optional

try:
    from app import db
except Exception:
    import db

try:
    from app.models.resurrecion import Resurrecion
except Exception:
    from models.resurrecion import Resurrecion

def get_resurrecion_by_id(idResu: int) -> Optional[Resurrecion]:
    """Recupera una resurrecion por id usando la conexión definida en app/db.py.

    Retorna una instancia de `Resurrecion` o `None` si no existe.
    """
    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idResu AS idResu, nombreResu FROM Resurrecion WHERE idResu = %s",
            (idResu,)
        )
        row = cur.fetchone()
    finally:
        cur.close()

    if not row:
        return None

    return Resurrecion(**row)