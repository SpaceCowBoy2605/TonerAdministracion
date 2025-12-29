from typing import Optional

try:
    from app import db
except Exception:
    import db

try:
    from app.models.planta import Planta
except Exception:
    from models.planta import Planta

def get_all_planta() -> Optional[Planta]:
    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idPlanta AS id, nombrePlanta FROM planta"
        )
        rows = cur.fetchall()
    finally:
        cur.close()

    if not rows:
        return None

    plantas = [Planta(**row) for row in rows]
    return plantas

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


def create_planta(data: dict) -> dict:
    """Crea una planta a partir de `data`, inserta en la BD y devuelve un dict."""
    planta = Planta(**data)

    cur = db.mydb.cursor()
    try:
        cur.execute(
            "INSERT INTO planta (nombrePlanta) VALUES (%s)",
            (planta.nombrePlanta,)
        )
        db.mydb.commit()
        planta.id = cur.lastrowid
    finally:
        cur.close()

    return planta.dict()

def update_planta(idPlanta: int, data: dict) -> bool:
    """Actualiza la planta con `idPlanta` usando `data`. Devuelve True si se actualizó."""
    planta = get_planta_by_id(idPlanta)
    if not planta:
        return False

    for key, value in data.items():
        setattr(planta, key, value)

    cur = db.mydb.cursor()
    try:
        cur.execute(
            "UPDATE planta SET nombrePlanta = %s WHERE idPlanta = %s",
            (planta.nombrePlanta, idPlanta)
        )
        db.mydb.commit()
    finally:
        cur.close()

    return True

def delete_planta(idPlanta: int) -> bool:
    """Elimina la planta con `idPlanta`. Devuelve True si se eliminó."""
    planta = get_planta_by_id(idPlanta)
    if not planta:
        return False

    cur = db.mydb.cursor()
    try:
        cur.execute(
            "DELETE FROM planta WHERE idPlanta = %s",
            (idPlanta,)
        )
        db.mydb.commit()
    finally:
        cur.close()

    return True