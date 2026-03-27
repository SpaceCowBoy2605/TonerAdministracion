from flask import Blueprint, jsonify

cedis_bp = Blueprint('Cedis', __name__)

@cedis_bp.route('/cedis/<int:id>', methods=['GET'])
def api_get_cedis(id):
    # importe aquí para evitar importaciones circulares
    from app.crud.cedis_crud import get_cedis_by_id
    Cedis = get_cedis_by_id(id)
    if not Cedis:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(Cedis.dict()), 200

@cedis_bp.route('/cedis', methods=['GET'])
def api_get_all_cedis():
    # importe aquí para evitar importaciones circulares
    from app.crud.cedis_crud import get_all_cedis
    Cedis_list = get_all_cedis()
    if not Cedis_list:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify([cedis.dict() for cedis in Cedis_list]), 200