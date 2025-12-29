from typing import Optional

try:
    from app import db
except Exception:
    import db

try:
    from app.models.impresora import Impresora
except Exception:
    from models.impresora import Impresora

def get_impresora_by_id(idImpresora: int) -> Optional[Impresora]:

    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idImpresora AS id, nombreImpresora, modelo FROM impresora WHERE idImpresora = %s",
            (idImpresora,)
        )
        row = cur.fetchone()
    finally:
        cur.close()

    if not row:
        return None

    return Impresora(**row)