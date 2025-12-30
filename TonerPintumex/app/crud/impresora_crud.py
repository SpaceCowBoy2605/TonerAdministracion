from typing import Optional

try:
    from app import db
except Exception:
    import db

try:
    from app.models.impresora import Impresora
except Exception:
    from models.impresora import Impresora


def get_all_impresora() -> Optional[Impresora]:
    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idImpresora AS id, nombreImpresora, modelo FROM impresora"
        )
        rows = cur.fetchall()
    finally:
        cur.close()

    if not rows:
        return None

    impresoras = [Impresora(**row) for row in rows]
    return impresoras

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

def create_impresora(data: dict) -> dict:
    """Crea una impresora a partir de `data`, inserta en la BD y devuelve un dict."""
    impresora = Impresora(**data)

    cur = db.mydb.cursor()
    try:
        cur.execute(
            "INSERT INTO impresora (nombreImpresora, modelo, idAccesorio, idCedis, idPlanta, idResurreccion, idTep) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (impresora.nombreImpresora, impresora.modelo)
        )
        db.mydb.commit()
        impresora.id = cur.lastrowid 
    finally:
        cur.close()

    return impresora.dict()