from typing import Optional

try:
    from app import db
except Exception:
    import db

try:
    from app.models.factura import Factura
except Exception:
    from models.factura import Factura

def get_factura_by_id(idfactura: int) -> Optional[Factura]:
    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idfactura AS id, fecha FROM factura WHERE idfactura = %s",
            (idfactura,)
        )
        row = cur.fetchone()
    finally:
        cur.close()

    if not row:
        return None

    return Factura(**row)

def get_all_factura() -> Optional[Factura]:
    cur = db.mydb.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT idfactura AS id, fecha FROM factura"
        )
        rows = cur.fetchall()
    finally:
        cur.close()

    if not rows:
        return None

    facturas = [Factura(**row) for row in rows]
    return facturas