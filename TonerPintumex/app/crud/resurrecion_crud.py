from typing import Optional

try:
    from app import db
except Exception:
    import db

try:
    from app.models.resu import Resurrecion
except Exception:
    from models.resu import Resurrecion

def get_resurrecion_by_id(idResu: int) -> Optional[Resurrecion]:

    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idResu AS id, nombreResu FROM resurreccion WHERE idResu = %s",
            (idResu,)
        )
        row = cur.fetchone()
    finally:
        cur.close()

    if not row:
        return None

    return Resurrecion(**row)