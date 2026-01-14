from typing import Optional
import os
import json
import logging

try:
    from app import db
except Exception:
    import db

try:
    from app.models.solicitudes import Solicitudes
except Exception:
    from models.solicitudes import Solicitudes


def _row_to_solicitud_dict(row: dict) -> dict:
    out: dict = {k: row.get(k) for k in (
        "id",
        "idAccesorio",
        "idImpresora",
        "cantidad",
        "fechaSolicitud",
        "centroCostos",
        "idPlanta",
        "idResu",
        "idCedis",
        "idTep",
    )}

    # Accesorio (con estatus + factura)
    if row.get("acc_id") is not None:
        accesorio = {
            "id": row.get("acc_id"),
            "nombreAccesorio": row.get("acc_nombreAccesorio"),
            "cantidad": row.get("acc_cantidad"),
            "idEstatus": row.get("acc_idEstatus"),
            "entrada": row.get("acc_entrada"),
            "idfactura": row.get("acc_idfactura"),
        }

        if row.get("est_id") is not None:
            accesorio["estatus"] = {
                "id": row.get("est_id"),
                "estatus": row.get("est_estatus"),
            }
        else:
            accesorio["estatus"] = None

        if row.get("fac_id") is not None:
            accesorio["factura"] = {
                "id": row.get("fac_id"),
                "fecha": row.get("fac_fecha"),
            }
        else:
            accesorio["factura"] = None

        out["accesorio"] = accesorio
    else:
        out["accesorio"] = None

    # Impresora (y sus relaciones)
    if row.get("imp_id") is not None:
        impresora = {
            "id": row.get("imp_id"),
            "nombreImpresora": row.get("imp_nombreImpresora"),
            "modelo": row.get("imp_modelo"),
            "idAccesorio": row.get("imp_idAccesorio"),
            "idCedis": row.get("imp_idCedis"),
            "idPlanta": row.get("imp_idPlanta"),
            "idResu": row.get("imp_idResu"),
            "idTep": row.get("imp_idTep"),
        }

        if row.get("imp_acc_id") is not None:
            impresora["accesorio"] = {
                "id": row.get("imp_acc_id"),
                "nombreAccesorio": row.get("imp_acc_nombreAccesorio"),
                "cantidad": row.get("imp_acc_cantidad"),
                "idEstatus": row.get("imp_acc_idEstatus"),
                "entrada": row.get("imp_acc_entrada"),
                "idfactura": row.get("imp_acc_idfactura"),
            }
        else:
            impresora["accesorio"] = None

        if row.get("imp_ced_id") is not None:
            impresora["cedis"] = {
                "id": row.get("imp_ced_id"),
                "nombreCedis": row.get("imp_ced_nombreCedis"),
            }
        else:
            impresora["cedis"] = None

        if row.get("imp_pla_id") is not None:
            impresora["planta"] = {
                "id": row.get("imp_pla_id"),
                "nombrePlanta": row.get("imp_pla_nombrePlanta"),
            }
        else:
            impresora["planta"] = None

        if row.get("imp_res_id") is not None:
            impresora["resu"] = {
                "id": row.get("imp_res_id"),
                "nombreResu": row.get("imp_res_nombreResu"),
            }
        else:
            impresora["resu"] = None

        if row.get("imp_tep_id") is not None:
            impresora["tep"] = {
                "id": row.get("imp_tep_id"),
                "nombreTep": row.get("imp_tep_nombreTep"),
            }
        else:
            impresora["tep"] = None

        out["impresora"] = impresora
    else:
        out["impresora"] = None

    # Ubicación solicitada (si viene)
    if row.get("s_pla_id") is not None:
        out["planta"] = {"id": row.get("s_pla_id"), "nombrePlanta": row.get("s_pla_nombrePlanta")}
    else:
        out["planta"] = None

    if row.get("s_res_id") is not None:
        out["resu"] = {"id": row.get("s_res_id"), "nombreResu": row.get("s_res_nombreResu")}
    else:
        out["resu"] = None

    if row.get("s_ced_id") is not None:
        out["cedis"] = {"id": row.get("s_ced_id"), "nombreCedis": row.get("s_ced_nombreCedis")}
    else:
        out["cedis"] = None

    if row.get("s_tep_id") is not None:
        out["tep"] = {"id": row.get("s_tep_id"), "nombreTep": row.get("s_tep_nombreTep")}
    else:
        out["tep"] = None

    return out

def get_all_solicitudes() -> Optional[list[Solicitudes]]:
    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT
                s.idSolicitud AS id,
                s.idAccesorio,
                s.idImpresora,
                s.cantidad,
                s.fechaSolicitud,
                s.centroCostos,
                s.idPlanta,
                s.idResu,
                s.idCedis,
                s.idTep,

                a.idAccesorio AS acc_id,
                a.nombreAccesorio AS acc_nombreAccesorio,
                a.cantidad AS acc_cantidad,
                a.idEstatus AS acc_idEstatus,
                a.entrada AS acc_entrada,
                a.idfactura AS acc_idfactura,
                e.idEstatus AS est_id,
                e.estatus AS est_estatus,
                f.idfactura AS fac_id,
                f.fecha AS fac_fecha,

                i.idImpresora AS imp_id,
                i.nombreImpresora AS imp_nombreImpresora,
                i.modelo AS imp_modelo,
                i.idAccesorio AS imp_idAccesorio,
                i.idCedis AS imp_idCedis,
                i.idPlanta AS imp_idPlanta,
                i.idResu AS imp_idResu,
                i.idTep AS imp_idTep,

                ia.idAccesorio AS imp_acc_id,
                ia.nombreAccesorio AS imp_acc_nombreAccesorio,
                ia.cantidad AS imp_acc_cantidad,
                ia.idEstatus AS imp_acc_idEstatus,
                ia.entrada AS imp_acc_entrada,
                ia.idfactura AS imp_acc_idfactura,

                ic.idCedis AS imp_ced_id,
                ic.nombreCedis AS imp_ced_nombreCedis,

                ip.idPlanta AS imp_pla_id,
                ip.nombrePlanta AS imp_pla_nombrePlanta,

                ir.idResu AS imp_res_id,
                ir.nombreResu AS imp_res_nombreResu,

                it.idTep AS imp_tep_id,
                it.nombreTep AS imp_tep_nombreTep,

                sp.idPlanta AS s_pla_id,
                sp.nombrePlanta AS s_pla_nombrePlanta,
                sr.idResu AS s_res_id,
                sr.nombreResu AS s_res_nombreResu,
                sc.idCedis AS s_ced_id,
                sc.nombreCedis AS s_ced_nombreCedis,
                st.idTep AS s_tep_id,
                st.nombreTep AS s_tep_nombreTep
            FROM solicitudes s
            LEFT JOIN accesorio a ON s.idAccesorio = a.idAccesorio
            LEFT JOIN estatus e ON a.idEstatus = e.idEstatus
            LEFT JOIN factura f ON a.idfactura = f.idfactura
            LEFT JOIN impresora i ON s.idImpresora = i.idImpresora
            LEFT JOIN accesorio ia ON i.idAccesorio = ia.idAccesorio
            LEFT JOIN cedis ic ON i.idCedis = ic.idCedis
            LEFT JOIN planta ip ON i.idPlanta = ip.idPlanta
            LEFT JOIN resurreccion ir ON i.idResu = ir.idResu
            LEFT JOIN teps it ON i.idTep = it.idTep
            LEFT JOIN planta sp ON s.idPlanta = sp.idPlanta
            LEFT JOIN resurreccion sr ON s.idResu = sr.idResu
            LEFT JOIN cedis sc ON s.idCedis = sc.idCedis
            LEFT JOIN teps st ON s.idTep = st.idTep
            ORDER BY s.idSolicitud DESC
            """
        )
        rows = cur.fetchall()
    finally:
        cur.close()
    
    if not rows:
        return None
    
    solicitudes = [Solicitudes(**_row_to_solicitud_dict(row)) for row in rows]
    return solicitudes

def get_solicitudes_by_id(idSolicitudes: int) -> Optional[Solicitudes]:

    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT
                s.idSolicitud AS id,
                s.idAccesorio,
                s.idImpresora,
                s.cantidad,
                s.fechaSolicitud,
                s.centroCostos,
                s.idPlanta,
                s.idResu,
                s.idCedis,
                s.idTep,

                a.idAccesorio AS acc_id,
                a.nombreAccesorio AS acc_nombreAccesorio,
                a.cantidad AS acc_cantidad,
                a.idEstatus AS acc_idEstatus,
                a.entrada AS acc_entrada,
                a.idfactura AS acc_idfactura,
                e.idEstatus AS est_id,
                e.estatus AS est_estatus,
                f.idfactura AS fac_id,
                f.fecha AS fac_fecha,

                i.idImpresora AS imp_id,
                i.nombreImpresora AS imp_nombreImpresora,
                i.modelo AS imp_modelo,
                i.idAccesorio AS imp_idAccesorio,
                i.idCedis AS imp_idCedis,
                i.idPlanta AS imp_idPlanta,
                i.idResu AS imp_idResu,
                i.idTep AS imp_idTep,

                ia.idAccesorio AS imp_acc_id,
                ia.nombreAccesorio AS imp_acc_nombreAccesorio,
                ia.cantidad AS imp_acc_cantidad,
                ia.idEstatus AS imp_acc_idEstatus,
                ia.entrada AS imp_acc_entrada,
                ia.idfactura AS imp_acc_idfactura,

                ic.idCedis AS imp_ced_id,
                ic.nombreCedis AS imp_ced_nombreCedis,

                ip.idPlanta AS imp_pla_id,
                ip.nombrePlanta AS imp_pla_nombrePlanta,

                ir.idResu AS imp_res_id,
                ir.nombreResu AS imp_res_nombreResu,

                it.idTep AS imp_tep_id,
                it.nombreTep AS imp_tep_nombreTep,

                sp.idPlanta AS s_pla_id,
                sp.nombrePlanta AS s_pla_nombrePlanta,
                sr.idResu AS s_res_id,
                sr.nombreResu AS s_res_nombreResu,
                sc.idCedis AS s_ced_id,
                sc.nombreCedis AS s_ced_nombreCedis,
                st.idTep AS s_tep_id,
                st.nombreTep AS s_tep_nombreTep
            FROM solicitudes s
            LEFT JOIN accesorio a ON s.idAccesorio = a.idAccesorio
            LEFT JOIN estatus e ON a.idEstatus = e.idEstatus
            LEFT JOIN factura f ON a.idfactura = f.idfactura
            LEFT JOIN impresora i ON s.idImpresora = i.idImpresora
            LEFT JOIN accesorio ia ON i.idAccesorio = ia.idAccesorio
            LEFT JOIN cedis ic ON i.idCedis = ic.idCedis
            LEFT JOIN planta ip ON i.idPlanta = ip.idPlanta
            LEFT JOIN resurreccion ir ON i.idResu = ir.idResu
            LEFT JOIN teps it ON i.idTep = it.idTep
            LEFT JOIN planta sp ON s.idPlanta = sp.idPlanta
            LEFT JOIN resurreccion sr ON s.idResu = sr.idResu
            LEFT JOIN cedis sc ON s.idCedis = sc.idCedis
            LEFT JOIN teps st ON s.idTep = st.idTep
            WHERE s.idSolicitud = %s
            LIMIT 1
            """,
            (idSolicitudes,),
        )
        row = cur.fetchone()
    finally:
        cur.close()

    if not row:
        return None

    return Solicitudes(**_row_to_solicitud_dict(row))

def create_solicitudes(data: dict) -> dict:
    """Crea una solicitud a partir de `data`, inserta en la BD y devuelve un dict."""
    solicitud = Solicitudes(**data)

    cur = db.mydb.cursor()
    try:
        cur.execute(
            "INSERT INTO solicitudes (idAccesorio, idImpresora, cantidad, fechaSolicitud, centroCostos, idPlanta, idResu, idCedis, idTep) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                solicitud.idAccesorio,
                solicitud.idImpresora,
                solicitud.cantidad,
                solicitud.fechaSolicitud,
                solicitud.centroCostos,
                solicitud.idPlanta,
                solicitud.idResu,
                solicitud.idCedis,
                solicitud.idTep
            )
        )
        db.mydb.commit()
        solicitud.id = cur.lastrowid
    finally:
        cur.close()

    return solicitud.dict()

def update_solicitudes(idSolicitudes: int, data: dict) -> Optional[dict]:
    solicitud = get_solicitudes_by_id(idSolicitudes)
    if not solicitud:
        return None

    updated_solicitud = solicitud.copy(update=data)

    cur = db.mydb.cursor()
    try:
        cur.execute(
            "UPDATE solicitudes SET idAccesorio = %s, idImpresora = %s, cantidad = %s, fechaSolicitud = %s, centroCostos = %s, idPlanta = %s, idResu = %s, idCedis = %s, idTep = %s WHERE idSolicitud = %s",
            (
                updated_solicitud.idAccesorio,
                updated_solicitud.idImpresora,
                updated_solicitud.cantidad,
                updated_solicitud.fechaSolicitud,
                updated_solicitud.centroCostos,
                updated_solicitud.idPlanta,
                updated_solicitud.idResu,
                updated_solicitud.idCedis,
                updated_solicitud.idTep,
                idSolicitudes
            )
        )
        db.mydb.commit()
    finally:
        cur.close()

    return updated_solicitud.dict()

def delete_solicitudes(idSolicitudes: int) -> bool:
    cur = db.mydb.cursor()
    try:
        cur.execute(
            "DELETE FROM solicitudes WHERE idSolicitud = %s",
            (idSolicitudes,)
        )
        db.mydb.commit()
        deleted = cur.rowcount > 0
    finally:
        cur.close()

    return deleted