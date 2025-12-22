from typing import Optional

try:
    from app import db
except Exception:
    import db

try:
    from app.models.planta import Planta
except Exception:
    from models.planta import Planta

def get_tep_by_id(idTep: int) -> Optional[Planta]:

    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idTep AS id, nombreTep FROM tep WHERE idTep = %s",
            (idTep,)
        )
        row = cur.fetchone()
    finally:
        cur.close()

    if not row:
        return None

    return Planta(**row)