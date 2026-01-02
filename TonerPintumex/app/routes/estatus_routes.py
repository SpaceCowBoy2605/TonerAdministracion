from flask import Blueprint, jsonify

estatus_bp = Blueprint('Estatus', __name__)

@estatus_bp.route('/estatus/<int:id>', methods=['GET'])
def api_get_estatus(id):
    # importe aquí para evitar importaciones circulares
    from crud.esatus_crud import get_estatus_by_id
    Estatus = get_estatus_by_id(id)
    if not Estatus:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(Estatus.dict()), 200

@estatus_bp.route('/estatus', methods=['GET'])
def api_get_all_estatus():
    # importe aquí para evitar importaciones circulares
    from crud.esatus_crud import get_all_estatus
    Estatus_list = get_all_estatus()
    if not Estatus_list:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify([estatus.dict() for estatus in Estatus_list]), 200