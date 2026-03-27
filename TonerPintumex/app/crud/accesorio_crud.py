from typing import Optional
import os
import json
import logging
from datetime import datetime
import io
import base64
from flask import url_for, current_app, has_app_context

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
    from app.models.accesorio import Accesorio


def _row_to_accesorio_dict(row: dict) -> dict:
    out: dict = {k: row.get(k) for k in (
        "id",
        "nombreAccesorio",
        "cantidad",
        "idEstatus",
        "entrada",
        "idfactura",
    )}

    def _calc_idestatus(cantidad: int) -> int:
        # Catálogo (según BD): 1=Suficiente, 2=Bajo, 3=Solicitar mas, 4=Reservado
        if cantidad >= 6:
            return 1
        if cantidad >= 3:
            return 2
        return 3

    def _label_for_idestatus(id_estatus: int) -> str:
        return {
            1: "Sufuciente",
            2: "Bajo",
            3: "Solcitar mas",
            4: "Reservado",
        }.get(id_estatus, "")

    def attach(name: str, id_key: str, fields: dict[str, str]) -> None:
        rel_id = row.get(id_key)
        if rel_id is None:
            return
        out[name] = {"id": rel_id, **{k: row.get(v) for k, v in fields.items()}}

    # Normalizar estatus desde cantidad para evitar inversiones por datos viejos.
    try:
        if out.get("cantidad") is not None:
            computed_id = _calc_idestatus(int(out["cantidad"]))
            out["idEstatus"] = computed_id
            joined_id = row.get("est_id")
            joined_label = row.get("est_estatus")
            out["estatus"] = {
                "id": computed_id,
                "estatus": joined_label if joined_id == computed_id else _label_for_idestatus(computed_id),
            }
        else:
            attach("estatus", "est_id", {"estatus": "est_estatus"})
    except Exception:
        attach("estatus", "est_id", {"estatus": "est_estatus"})
    attach("factura", "fac_id", {"fecha": "fac_fecha"})
    return out

def get_all_accesorio() -> Optional[list[Accesorio]]:
    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT
                a.idAccesorio AS id,
                a.nombreAccesorio,
                a.cantidad,
                a.idEstatus,
                a.entrada,
                a.idfactura,

                e.idEstatus AS est_id,
                e.estatus AS est_estatus,

                f.idfactura AS fac_id,
                f.fecha AS fac_fecha
            FROM accesorio a
            LEFT JOIN estatus e ON a.idEstatus = e.idEstatus
            LEFT JOIN factura f ON a.idfactura = f.idfactura
            """
        )
        rows = cur.fetchall()
    finally:
        cur.close()

    if not rows:
        return None

    accesorios = [Accesorio(**_row_to_accesorio_dict(row)) for row in rows]
    return accesorios

def get_accesorio_by_id(idAccesorio: int) -> Optional[Accesorio]:

    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT
                a.idAccesorio AS id,
                a.nombreAccesorio,
                a.cantidad,
                a.idEstatus,
                a.entrada,
                a.idfactura,

                e.idEstatus AS est_id,
                e.estatus AS est_estatus,

                f.idfactura AS fac_id,
                f.fecha AS fac_fecha
            FROM accesorio a
            LEFT JOIN estatus e ON a.idEstatus = e.idEstatus
            LEFT JOIN factura f ON a.idfactura = f.idfactura
            WHERE a.idAccesorio = %s
            """ ,
            (idAccesorio,)
        )
        row = cur.fetchone()
    finally:
        cur.close()

    if not row:
        return None

    return Accesorio(**_row_to_accesorio_dict(row))


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
    qr_base64 = None
    try:
        if qrcode is None:
            logging.warning("qrcode library not available — no QR will be generated for accesorio %s", getattr(accesorio, 'id', None))
        else:
            # Determinar carpeta static de la app (cuando hay contexto), sino caer a ../static
            try:
                if has_app_context():
                    static_folder = current_app.static_folder
                else:
                    static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
            except Exception:
                static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

            qr_dir = os.path.join(static_folder, 'accesorio_qrcodes')
            os.makedirs(qr_dir, exist_ok=True)
            # Contenido multilínea con etiquetas
            content = (
                f"{accesorio.id}\n"
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
                        # También generar la imagen en memoria y codificarla en base64
            try:
                buf = io.BytesIO()
                img.save(buf, format='PNG')
                buf.seek(0)
                b64 = base64.b64encode(buf.getvalue()).decode('ascii')
                qr_base64 = f"data:image/png;base64,{b64}"
            except Exception:
                logging.exception("Failed to encode QR to base64 for accesorio %s", getattr(accesorio, 'id', None))
                qr_base64 = None
    except Exception:
        logging.exception("Failed to generate QR for accesorio %s", getattr(accesorio, 'id', None))
        qr_path = None
        qr_base64 = None

    qr_url = None
    if qr_path:
        try:
            if has_app_context():
                # Servir desde /static/accesorio_qrcodes/<filename>
                qr_url = url_for('static', filename=f"accesorio_qrcodes/{filename}", _external=True)
            else:
                qr_url = None
        except Exception:
            logging.exception("Failed to build qr_url for accesorio %s", getattr(accesorio, 'id', None))
            qr_url = None

    result = accesorio.dict()
    result['qr_path'] = qr_path
    result['qr_base64'] = qr_base64
    result["qr_url"] = qr_url
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
        # Catálogo (según BD): 1=Suficiente, 2=Bajo, 3=Solicitar mas, 4=Reservado
        if accesorio.cantidad >= 6:
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
