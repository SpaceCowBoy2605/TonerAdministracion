from typing import Optional
import os

try:
    import qrcode
except Exception:
    qrcode = None

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
            "INSERT INTO impresora (nombreImpresora, modelo, idAccesorio, idCedis, idPlanta, idResu, idTep) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                impresora.nombreImpresora,
                impresora.modelo,
                impresora.idAccesorio,
                impresora.idCedis,
                impresora.idPlanta,
                impresora.idResu,
                impresora.idTep,
            )
        )
        db.mydb.commit()
        impresora.id = cur.lastrowid 
    finally:
        cur.close()

    # Generar QR con nombre y modelo (si está disponible la librería)
    qr_path = None
    try:
        if qrcode is not None:
            qr_dir = os.path.join(os.getcwd(), 'impresora_qrcodes')
            os.makedirs(qr_dir, exist_ok=True)
            content = f"{impresora.nombreImpresora} - {impresora.modelo }"
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(content)
            qr.make(fit=True)
            img = qr.make_image(fill_color='black', back_color='white')
            filename = f"impresora_{impresora.id}.png"
            qr_path = os.path.join(qr_dir, filename)
            img.save(qr_path)
    except Exception:
        qr_path = None

    result = impresora.dict()
    # result['qr_path'] = qr_path
    return result


def update_impresora(idImpresora: int, data: dict) -> bool:
    """Actualiza la impresora con `idImpresora` usando `data`. Devuelve True si se actualizó."""
    impresora = get_impresora_by_id(idImpresora)
    if not impresora:
        return False

    for key, value in data.items():
        setattr(impresora, key, value)

    cur = db.mydb.cursor()
    try:
        cur.execute(
            "UPDATE impresora SET nombreImpresora = %s, modelo = %s WHERE idImpresora = %s",
            (impresora.nombreImpresora, impresora.modelo, idImpresora)
        )
        db.mydb.commit()
    finally:
        cur.close()

    return True


def delete_impresora(idImpresora: int) -> bool:
    """Elimina la impresora con `idImpresora`. Devuelve True si se eliminó."""
    impresora = get_impresora_by_id(idImpresora)
    if not impresora:
        return False

    cur = db.mydb.cursor()
    try:
        cur.execute(
            "DELETE FROM impresora WHERE idImpresora = %s",
            (idImpresora,)
        )
        db.mydb.commit()
    finally:
        cur.close()

    return True