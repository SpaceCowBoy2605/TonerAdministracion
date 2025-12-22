from typing import Optional

try:
    from app import db
except Exception:
    import db

try:
    from app.models.planta import Planta
except Exception:
    from models.planta import Planta

def get_planta_by_id(idPlanta: int) -> Optional[Planta]:

    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idPlanta AS id, nombrePlanta FROM planta WHERE idPlanta = %s",
            (idPlanta,)
        )
        row = cur.fetchone()
    finally:
        cur.close()

    if not row:
        return None

    return Planta(**row)