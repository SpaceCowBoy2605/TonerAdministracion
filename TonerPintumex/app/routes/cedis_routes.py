from flask import Blueprint, jsonify

cedis_bp = Blueprint('cedis', __name__)


@cedis_bp.route('/cedis/<int:id>', methods=['GET'])
def api_get_cedis(id):
    # importe aquí para evitar importaciones circulares
    from crud.cedis_crud import get_cedis_by_id
    cedis = get_cedis_by_id(id)
    if not cedis:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(cedis.dict()), 200
