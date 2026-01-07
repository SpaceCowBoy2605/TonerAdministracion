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

def get_all_solicitudes() -> Optional[Solicitudes]:
    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idSolicitud AS id, idAccesorio, idImpresora, cantidad, fechaSolicitud, centroCostos, idPlanta, idResu, idCedis, idTep FROM solicitudes"
        )
        rows = cur.fetchall()
    finally:
        cur.close()
    
    if not rows:
        return None
    
    solicitudes = [Solicitudes(**row) for row in rows]
    return solicitudes

def get_solicitudes_by_id(idSolicitudes: int) -> Optional[Solicitudes]:

    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idSolicitud AS id, idAccesorio, idImpresora, cantidad, fechaSolicitud, centroCostos, idPlanta, idResu, idCedis, idTep FROM solicitudes WHERE idSolicitud = %s",
            (idSolicitudes,)
        )
        row = cur.fetchone()
    finally:
        cur.close()

    if not row:
        return None

    return Solicitudes(**row)

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
            "DELETE FROM solicitudes WHERE idSolicitudes = %s",
            (idSolicitudes,)
        )
        db.mydb.commit()
        deleted = cur.rowcount > 0
    finally:
        cur.close()

    return deleted