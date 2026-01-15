from typing import Optional
import os
import logging

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

def _row_to_impresora_dict(row: dict) -> dict:
    """Convierte una fila (con aliases de JOIN) a un dict compatible con `Impresora`."""

    out: dict = {k: row.get(k) for k in (
        "id",
        "nombreImpresora",
        "modelo",
        "idAccesorio",
        "idCedis",
        "idPlanta",
        "idResu",
        "idTep",
    )}

    def attach(name: str, id_key: str, fields: dict[str, str]) -> None:
        rel_id = row.get(id_key)
        if rel_id is None:
            return
        out[name] = {"id": rel_id, **{k: row.get(v) for k, v in fields.items()}}

    attach(
        "accesorio",
        "acc_id",
        {
            "nombreAccesorio": "acc_nombreAccesorio",
            "cantidad": "acc_cantidad",
            "idEstatus": "acc_idEstatus",
            "entrada": "acc_entrada",
            "idfactura": "acc_idfactura",
        },
    )
    attach("cedis", "ced_id", {"nombreCedis": "ced_nombreCedis"})
    attach("planta", "pla_id", {"nombrePlanta": "pla_nombrePlanta"})
    attach("resu", "res_id", {"nombreResu": "res_nombreResu"})
    attach("tep", "tep_id", {"nombreTep": "tep_nombreTep"})

    return out


def get_all_impresora() -> Optional[list[Impresora]]:
    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT
                i.idImpresora AS id,
                i.nombreImpresora,
                i.modelo,
                i.idAccesorio,
                i.idCedis,
                i.idPlanta,
                i.idResu,
                i.idTep,

                a.idAccesorio AS acc_id,
                a.nombreAccesorio AS acc_nombreAccesorio,
                a.cantidad AS acc_cantidad,
                a.idEstatus AS acc_idEstatus,
                a.entrada AS acc_entrada,
                a.idfactura AS acc_idfactura,

                c.idCedis AS ced_id,
                c.nombreCedis AS ced_nombreCedis,

                p.idPlanta AS pla_id,
                p.nombrePlanta AS pla_nombrePlanta,

                r.idResu AS res_id,
                r.nombreResu AS res_nombreResu,

                t.idTep AS tep_id,
                t.nombreTep AS tep_nombreTep
            FROM impresora i
            LEFT JOIN accesorio a ON i.idAccesorio = a.idAccesorio
            LEFT JOIN cedis c ON i.idCedis = c.idCedis
            LEFT JOIN planta p ON i.idPlanta = p.idPlanta
            LEFT JOIN resurreccion r ON i.idResu = r.idResu
            LEFT JOIN teps t ON i.idTep = t.idTep
            """
        )
        rows = cur.fetchall()
    finally:
        cur.close()

    if not rows:
        return None

    impresoras = [Impresora(**_row_to_impresora_dict(row)) for row in rows]
    return impresoras

def get_impresora_by_id(idImpresora: int) -> Optional[Impresora]:

    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT
                i.idImpresora AS id,
                i.nombreImpresora,
                i.modelo,
                i.idAccesorio,
                i.idCedis,
                i.idPlanta,
                i.idResu,
                i.idTep,

                a.idAccesorio AS acc_id,
                a.nombreAccesorio AS acc_nombreAccesorio,
                a.cantidad AS acc_cantidad,
                a.idEstatus AS acc_idEstatus,
                a.entrada AS acc_entrada,
                a.idfactura AS acc_idfactura,

                c.idCedis AS ced_id,
                c.nombreCedis AS ced_nombreCedis,

                p.idPlanta AS pla_id,
                p.nombrePlanta AS pla_nombrePlanta,

                r.idResu AS res_id,
                r.nombreResu AS res_nombreResu,

                t.idTep AS tep_id,
                t.nombreTep AS tep_nombreTep
            FROM impresora i
            LEFT JOIN accesorio a ON i.idAccesorio = a.idAccesorio
            LEFT JOIN cedis c ON i.idCedis = c.idCedis
            LEFT JOIN planta p ON i.idPlanta = p.idPlanta
            LEFT JOIN resurreccion r ON i.idResu = r.idResu
            LEFT JOIN teps t ON i.idTep = t.idTep
            WHERE i.idImpresora = %s
            """,
            (idImpresora,),
        )
        row = cur.fetchone()
    finally:
        cur.close()

    if not row:
        return None

    return Impresora(**_row_to_impresora_dict(row))

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
        if qrcode is None:
            logging.warning("qrcode library not available — no QR will be generated for impresora %s", getattr(impresora, 'id', None))
        else:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
            qr_dir = os.path.join(base_dir, 'impresora_qrcodes')
            os.makedirs(qr_dir, exist_ok=True)
            content = (
                f"{impresora.id}\n"
                f"{impresora.nombreImpresora} - {impresora.modelo}"
            )
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(content)
            qr.make(fit=True)
            img = qr.make_image(fill_color='black', back_color='white')
            filename = f"impresora_{impresora.id}.png"
            qr_path = os.path.join(qr_dir, filename)
            img.save(qr_path)
    except Exception:
        logging.exception("Failed to generate QR for impresora %s", getattr(impresora, 'id', None))
        qr_path = None

    result = impresora.dict()
    result['qr_path'] = qr_path
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