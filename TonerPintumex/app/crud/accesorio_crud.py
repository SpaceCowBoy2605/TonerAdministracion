from typing import Optional
import os
import json
import logging
from datetime import datetime

try:
    import qrcode
except Exception:
    qrcode = None

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
            "SELECT idAccesorio AS id, nombreAccesorio, cantidad, idEstatus, entrada, idfactura FROM accesorio"
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
            "SELECT idAccesorio AS id, nombreAccesorio, cantidad, idEstatus, entrada, idfactura FROM accesorio WHERE idAccesorio = %s",
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
            "INSERT INTO accesorio (nombreAccesorio, cantidad, idEstatus, entrada, idfactura) VALUES (%s, %s, %s, %s, %s)",
            (accesorio.nombreAccesorio, accesorio.cantidad, accesorio.idEstatus, accesorio.entrada, accesorio.idfactura)
        )
        db.mydb.commit()
        accesorio.id = cur.lastrowid
    finally:
        cur.close()

    qr_path = None
    try:
        if qrcode is None:
            logging.warning("qrcode library not available — no QR will be generated for accesorio %s", getattr(accesorio, 'id', None))
        else:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
            qr_dir = os.path.join(base_dir, 'accesorio_qrcodes')
            os.makedirs(qr_dir, exist_ok=True)
            # Contenido multilínea con etiquetas
            content = (
                f"{accesorio.nombreAccesorio}\n"
                f"{accesorio.entrada}\n"
                f"{accesorio.idfactura}"
            )
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(content)
            qr.make(fit=True)
            img = qr.make_image(fill_color='black', back_color='white')
            filename = f"accesorio_{accesorio.id}.png"
            qr_path = os.path.join(qr_dir, filename)
            img.save(qr_path)
    except Exception:
        logging.exception("Failed to generate QR for accesorio %s", getattr(accesorio, 'id', None))
        qr_path = None

    result = accesorio.dict()
    result['qr_path'] = qr_path
    return result

def update_accesorio(idAccesorio: int, data: dict) -> Optional[dict]:
    """Actualiza un accesorio con `data` en la BD. Devuelve el dict del accesorio actualizado o None si no existe."""
    accesorio = get_accesorio_by_id(idAccesorio)
    if not accesorio:
        return None
    # Guardar cantidad antigua para registrar movimiento en historial
    cantidad_antigua = accesorio.cantidad
    idfactura_antigua = accesorio.idfactura

    # Si la request incluye 'cantidad', interpretarla como delta a sumar (no reemplazo)
    if 'cantidad' in data and data['cantidad'] is not None:
        try:
            delta = int(data['cantidad'])
        except Exception:
            delta = 0
        accesorio.cantidad = (cantidad_antigua or 0) + delta
        # Calcular estatus según la nueva cantidad (>=10:1, 3-9:2, <3:3)
        if accesorio.cantidad >= 10:
            accesorio.idEstatus = 1
        elif accesorio.cantidad >= 3:
            accesorio.idEstatus = 2
        else:
            accesorio.idEstatus = 3
        # eliminar la clave para no volver a aplicarla en el bucle siguiente
        data = {k: v for k, v in data.items() if k != 'cantidad'}

    for key, value in data.items():
        setattr(accesorio, key, value)

    cur = db.mydb.cursor()
    try:
        cur.execute(
            "UPDATE accesorio SET nombreAccesorio = %s, cantidad = %s, idEstatus = %s, entrada = %s, idfactura = %s WHERE idAccesorio = %s",
            (accesorio.nombreAccesorio, accesorio.cantidad, accesorio.idEstatus, accesorio.entrada, accesorio.idfactura, idAccesorio)
        )

        # Si la cantidad cambió, registrar la actualización en historialAccesorios
        try:
            nueva_cantidad = accesorio.cantidad
            if nueva_cantidad != cantidad_antigua:
                # registrar el delta (puede ser positivo o negativo)
                movimiento = nueva_cantidad - (cantidad_antigua or 0)
                fecha = datetime.now()
                cur.execute(
                    "INSERT INTO historialAccesorios (idfactura, idAccesorio, fecha, cantidad) VALUES (%s, %s, %s, %s)",
                    (idfactura_antigua, idAccesorio, fecha, movimiento)
                )
            # Asegurarse de que idEstatus esté actualizado también si no vino en data
            # si el usuario pasó idEstatus explícito, lo respetamos; si no, ya lo hemos calculado arriba cuando se proporcionó 'cantidad'
            if 'idEstatus' not in data:
                # recalcular por si la cantidad fue modificada por otros campos
                if accesorio.cantidad >= 10:
                    accesorio.idEstatus = 1
                elif accesorio.cantidad >= 3:
                    accesorio.idEstatus = 2
                else:
                    accesorio.idEstatus = 3
        except Exception:
            # Si falla el registro en historial, hacemos rollback para asegurar consistencia
            db.mydb.rollback()
            logging.exception("Failed to insert historialAccesorios during accesorio update for %s", idAccesorio)
            raise

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
