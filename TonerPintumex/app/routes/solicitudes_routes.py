from flask import Blueprint, jsonify

solicitudes_bp = Blueprint('solicitudes', __name__)


def _dump_solicitud(model) -> dict:
    data = model.model_dump() if hasattr(model, 'model_dump') else model.dict()

    def drop_fk_if_nested(fk_key: str, nested_key: str) -> None:
        if data.get(nested_key) is not None:
            data.pop(fk_key, None)
        if data.get(fk_key) is None:
            data.pop(fk_key, None)

    def _clean_accesorio(accesorio: dict | None) -> None:
        if not isinstance(accesorio, dict):
            return

        # En el modelo `Accesorio`, `idEstatus` es requerido; se conserva en el CRUD
        # y aquí se elimina solo si ya existe `estatus`.
        if accesorio.get('estatus') is not None:
            accesorio.pop('idEstatus', None)
        if accesorio.get('idEstatus') is None:
            accesorio.pop('idEstatus', None)

        if accesorio.get('factura') is not None:
            accesorio.pop('idfactura', None)
        if accesorio.get('idfactura') is None:
            accesorio.pop('idfactura', None)

    def _clean_impresora(impresora: dict | None) -> None:
        if not isinstance(impresora, dict):
            return

        def drop_imp_fk_if_nested(fk_key: str, nested_key: str) -> None:
            if impresora.get(nested_key) is not None:
                impresora.pop(fk_key, None)
            if impresora.get(fk_key) is None:
                impresora.pop(fk_key, None)

        drop_imp_fk_if_nested('idAccesorio', 'accesorio')
        drop_imp_fk_if_nested('idCedis', 'cedis')
        drop_imp_fk_if_nested('idPlanta', 'planta')
        drop_imp_fk_if_nested('idResu', 'resu')
        drop_imp_fk_if_nested('idTep', 'tep')

        _clean_accesorio(impresora.get('accesorio'))

    drop_fk_if_nested('idAccesorio', 'accesorio')
    drop_fk_if_nested('idImpresora', 'impresora')
    drop_fk_if_nested('idPlanta', 'planta')
    drop_fk_if_nested('idResu', 'resu')
    drop_fk_if_nested('idCedis', 'cedis')
    drop_fk_if_nested('idTep', 'tep')

    _clean_accesorio(data.get('accesorio'))
    _clean_impresora(data.get('impresora'))

    return data

@solicitudes_bp.route('/solicitudes', methods=['GET'])
def api_get_all_solicitudes():
    # importe aquí para evitar importaciones circulares
    from app.crud.solicitudes_crud import get_all_solicitudes
    solicitudes = get_all_solicitudes()
    if not solicitudes:
        return jsonify([]), 200
    return jsonify([_dump_solicitud(solicitud) for solicitud in solicitudes]), 200

@solicitudes_bp.route('/solicitudes/<int:id>', methods=['GET'])
def api_get_solicitudes(id):
    # importe aquí para evitar importaciones circulares
    from app.crud.solicitudes_crud import get_solicitudes_by_id
    solicitud = get_solicitudes_by_id(id)
    if not solicitud:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(_dump_solicitud(solicitud)), 200

@solicitudes_bp.route('/solicitudes/crear', methods=['POST'])
def api_create_solicitudes():
    # importe aquí para evitar importaciones circulares
    from services.solicitudes_service import create_solicitud_with_rules
    from flask import request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos inválidos"}), 400
    try:
        solicitud = create_solicitud_with_rules(data)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception:
        return jsonify({"error": "Error interno al crear la solicitud"}), 500
    return jsonify({"message": "Solicitud creada", "solicitud": solicitud}), 200

@solicitudes_bp.route('/solicitudes/actualizar/<int:id>', methods=['PUT'])
def api_update_solicitudes(id):
    # importe aquí para evitar importaciones circulares
    from app.crud.solicitudes_crud import update_solicitudes
    from flask import request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos inválidos"}), 400
    updated_solicitud = update_solicitudes(id, data)
    if not updated_solicitud:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify({"message": "Solicitud actualizada"}), 200

@solicitudes_bp.route('/solicitudes/eliminar/<int:id>', methods=['DELETE'])
def api_delete_solicitudes(id):
    # importe aquí para evitar importaciones circulares
    from app.crud.solicitudes_crud import delete_solicitudes
    deleted_solicitud = delete_solicitudes(id)
    if not deleted_solicitud:
        return jsonify({"error": "Solicitud no encontrada"}), 404
    return jsonify({"message": "Solicitud eliminada"}), 200