from typing import Optional

try:
    from app import db
except Exception:
    import db

try:
    from app.models.accesorio import Accesorio
except Exception:
    from models.accesorio import Accesorio

def get_all_accesorio() -> Optional[Accesorio]:
    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idAccesorio AS id, nombreAccesorio, cantidad, status, entrada FROM accesorio"
        )
        rows = cur.fetchall()
    finally:
        cur.close()

    if not rows:
        return None

    accesorios = [Accesorio(**row) for row in rows]
    return accesorios

def get_accesorio_by_id(idAccesorio: int) -> Optional[Accesorio]:

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


def create_accesorio(data: dict) -> dict:
    """Crea un accesorio a partir de `data`, inserta en la BD y devuelve un dict."""
    accesorio = Accesorio(**data)

    cur = db.mydb.cursor()
    try:
        cur.execute(
            "INSERT INTO accesorio (nombreAccesorio, cantidad, status, entrada) VALUES (%s, %s, %s, %s)",
            (accesorio.nombreAccesorio, accesorio.cantidad, accesorio.status, accesorio.entrada)
        )
        db.mydb.commit()
        accesorio.id = cur.lastrowid
    finally:
        cur.close()

    return accesorio.dict()

def update_accesorio(idAccesorio: int, data: dict) -> Optional[dict]:
    """Actualiza un accesorio con `data` en la BD. Devuelve el dict del accesorio actualizado o None si no existe."""
    accesorio = get_accesorio_by_id(idAccesorio)
    if not accesorio:
        return None

    for key, value in data.items():
        setattr(accesorio, key, value)

    cur = db.mydb.cursor()
    try:
        cur.execute(
            "UPDATE accesorio SET nombreAccesorio = %s, cantidad = %s, status = %s, entrada = %s WHERE idAccesorio = %s",
            (accesorio.nombreAccesorio, accesorio.cantidad, accesorio.status, accesorio.entrada, idAccesorio)
        )
        db.mydb.commit()
    finally:
        cur.close()

    return accesorio.dict()

def delete_accesorio(idAccesorio: int) -> bool:
    """Elimina el accesorio con `idAccesorio` de la BD. Devuelve True si se eliminó, False si no existe."""
    accesorio = get_accesorio_by_id(idAccesorio)
    if not accesorio:
        return False

    cur = db.mydb.cursor()
    try:
        cur.execute(
            "DELETE FROM accesorio WHERE idAccesorio = %s",
            (idAccesorio,)
        )
        db.mydb.commit()
    finally:
        cur.close()

    return True
