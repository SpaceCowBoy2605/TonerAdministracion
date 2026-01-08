from typing import Optional
import os
import json
import logging

try:
    from app import db
except Exception:
    import db

try:
    from app.models.historial import HistorialAccesorios
except Exception:
    from models.historial import HistorialAccesorios

def get_all_historial() -> Optional[HistorialAccesorios]:
    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idHistorial AS id, idfactura, idAccesorio, fecha, cantidad FROM historialAccesorios"
        )
        rows = cur.fetchall()
    finally:
        cur.close()

    if not rows:
        return None

    historiales = [HistorialAccesorios(**row) for row in rows]
    return historiales

def get_historial_by_id(idHistorial: int) -> Optional[HistorialAccesorios]:

    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idHistorial AS id, idfactura, idAccesorio, fecha, cantidad FROM historialAccesorios WHERE idHistorial = %s",
            (idHistorial,)
        )
        row = cur.fetchone()
    finally:
        cur.close()

    if not row:
        return None

    return Historial(**row)