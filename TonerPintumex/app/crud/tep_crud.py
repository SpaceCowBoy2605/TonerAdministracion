from typing import Optional

try:
    from app import db
except Exception:
    import db

try:
    from app.models.tep import Tep
except Exception:
    from models.tep import Tep

def get_tep_by_id(idTep: int) -> Optional[Tep]:

    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idTep AS id, nombreTep FROM teps WHERE idTep = %s",
            (idTep,)
        )
        row = cur.fetchone()
    finally:
        cur.close()

    if not row:
        return None

    return Tep(**row)