from flask import Blueprint, jsonify

solicitudes_bp = Blueprint('solicitudes', __name__)

@solicitudes_bp.route('/solicitudes', methods=['GET'])
def api_get_all_solicitudes():
    # importe aquí para evitar importaciones circulares
    from crud.solicitudes_crud import get_all_solicitudes
    solicitudes = get_all_solicitudes()
    if not solicitudes:
        return jsonify([]), 200
    return jsonify([solicitud.dict() for solicitud in solicitudes]), 200

@solicitudes_bp.route('/solicitudes/<int:id>', methods=['GET'])
def api_get_solicitudes(id):
    # importe aquí para evitar importaciones circulares
    from crud.solicitudes_crud import get_solicitudes_by_id
    solicitud = get_solicitudes_by_id(id)
    if not solicitud:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(solicitud.dict()), 200

@solicitudes_bp.route('/solicitudes/crear', methods=['POST'])
def api_create_solicitudes():
    # importe aquí para evitar importaciones circulares
    from crud.solicitudes_crud import create_solicitudes
    from flask import request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos inválidos"}), 400
    solicitud = create_solicitudes(data)
    return jsonify({"message": "Solicitud creada", "solicitud": solicitud}), 200

@solicitudes_bp.route('/solicitudes/actualizar/<int:id>', methods=['PUT'])
def api_update_solicitudes(id):
    # importe aquí para evitar importaciones circulares
    from crud.solicitudes_crud import update_solicitudes
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
    from crud.solicitudes_crud import delete_solicitudes
    deleted_solicitud = delete_solicitudes(id)
    if not deleted_solicitud:
        return jsonify({"error": "Solicitud no encontrada"}), 404
    return jsonify({"message": "Solicitud eliminada"}), 200