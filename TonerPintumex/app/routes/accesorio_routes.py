from flask import Blueprint, jsonify

accesorio_bp = Blueprint('accesorio', __name__)

@accesorio_bp.route('/accesorio', methods=['GET'])
def api_get_all_accesorios():
    # importe aquí para evitar importaciones circulares
    from crud.accesorio_crud import get_all_accesorio
    accesorios = get_all_accesorio()
    if not accesorios:
        return jsonify([]), 200
    return jsonify([accesorio.dict() for accesorio in accesorios]), 200

@accesorio_bp.route('/accesorio/<int:id>', methods=['GET'])
def api_get_accesorio(id):
    # importe aquí para evitar importaciones circulares
    from crud.accesorio_crud import get_accesorio_by_id
    accesorio = get_accesorio_by_id(id)
    if not accesorio:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(accesorio.dict()), 200

@accesorio_bp.route('/accesorio/crear', methods=['POST'])
def api_create_accesorio():
    # importe aquí para evitar importaciones circulares
    from crud.accesorio_crud import create_accesorio
    from flask import request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos inválidos"}), 400
    accesorio = create_accesorio(data)
    return jsonify({"message": "Accesorio creado", "accesorio": accesorio}), 200


@accesorio_bp.route('/accesorio/actualizar/<int:id>', methods=['PUT'])
def api_update_accesorio(id):
    # importe aquí para evitar importaciones circulares
    from crud.accesorio_crud import update_accesorio
    from flask import request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos inválidos"}), 400
    updated_accesorio = update_accesorio(id, data)
    if not updated_accesorio:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify({"message": "Accesorio actualizado"}), 200

@accesorio_bp.route('/accesorio/eliminar/<int:id>', methods=['DELETE'])
def api_delete_accesorio(id):
    # importe aquí para evitar importaciones circulares
    from crud.accesorio_crud import delete_accesorio
    deleted_accesorio = delete_accesorio(id)
    if not deleted_accesorio:
        return jsonify({"error": "Accesorio no encontrado"}), 404
    return jsonify({"message": "Accesorio eliminado"}), 200