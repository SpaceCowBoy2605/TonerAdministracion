from datetime import datetime
import logging

try:
    from app import db
except Exception:
    import db

try:
    from app.models.solicitudes import Solicitudes
except Exception:
    from models.solicitudes import Solicitudes


def create_solicitud_with_rules(data: dict) -> dict:
    """Crea una solicitud aplicando reglas de negocio:
    - verifica que el accesorio exista
    - verifica stock suficiente
    - decrementa la cantidad del accesorio
    - inserta la solicitud en la misma transacción
    Devuelve el dict de la solicitud creada.
    Lanza ValueError para condiciones esperadas (p. ej. stock insuficiente).
    """
    cur = db.mydb.cursor(dictionary=True)
    try:
        idAcc = data.get('idAccesorio')
        cantidad_solicitada = data.get('cantidad')
        if idAcc is None or cantidad_solicitada is None:
            raise ValueError('idAccesorio y cantidad son requeridos')

        # Bloquear fila del accesorio para evitar race conditions
        # Obtener también idfactura para registro en historial
        cur.execute("SELECT cantidad, idfactura FROM accesorio WHERE idAccesorio = %s FOR UPDATE", (idAcc,))
        row = cur.fetchone()
        if not row:
            raise ValueError('Accesorio no encontrado')

        cantidad_actual = row.get('cantidad')
        idfactura = row.get('idfactura')
        if cantidad_actual is None:
            raise ValueError('Accesorio sin cantidad definida')

        if cantidad_actual < cantidad_solicitada:
            raise ValueError('Stock insuficiente')

        nueva_cantidad = cantidad_actual - cantidad_solicitada

        # Determinar estatus según nueva cantidad y actualizar accesorio
        if nueva_cantidad >= 10:
            new_estatus = 1
        elif nueva_cantidad >= 3:
            new_estatus = 2
        else:
            new_estatus = 3
        cur.execute("UPDATE accesorio SET cantidad = %s, idEstatus = %s WHERE idAccesorio = %s", (nueva_cantidad, new_estatus, idAcc))

        # Preparar campos para insertar solicitud
        fecha = data.get('fechaSolicitud')
        if fecha is None:
            fecha = datetime.now()

        insert_values = (
            idAcc,
            data.get('idImpresora'),
            cantidad_solicitada,
            fecha,
            data.get('centroCostos'),
            data.get('idPlanta'),
            data.get('idResu'),
            data.get('idCedis'),
            data.get('idTep'),
        )

        cur.execute(
            "INSERT INTO solicitudes (idAccesorio, idImpresora, cantidad, fechaSolicitud, centroCostos, idPlanta, idResu, idCedis, idTep) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            insert_values
        )
        # Registrar en historialAccesorios el movimiento (donde 'cantidad' es la cantidad movida)
        try:
            cur.execute(
                "INSERT INTO historialAccesorios (idfactura, idAccesorio, fecha, cantidad) VALUES (%s, %s, %s, %s)",
                (idfactura, idAcc, fecha, cantidad_solicitada)
            )
        except Exception:
            # Si la tabla o campos no existen, registramos y continuamos (no queremos fallar la operación por el historial)
            logging.exception('Failed to insert into historialAccesorios')
        db.mydb.commit()
        nueva_id = cur.lastrowid

        solicitud_data = {
            'id': nueva_id,
            'idAccesorio': idAcc,
            'idImpresora': data.get('idImpresora'),
            'cantidad': cantidad_solicitada,
            'fechaSolicitud': fecha,
            'centroCostos': data.get('centroCostos'),
            'idPlanta': data.get('idPlanta'),
            'idResu': data.get('idResu'),
            'idCedis': data.get('idCedis'),
            'idTep': data.get('idTep'),
        }

        # Validar con el modelo pydantic
        solicitud = Solicitudes(**solicitud_data)
        return solicitud.dict()
    except Exception:
        try:
            db.mydb.rollback()
        except Exception:
            logging.exception('Failed to rollback transaction')
        logging.exception('Error creating solicitud with rules')
        raise
    finally:
        cur.close()
