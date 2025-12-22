from flask import Blueprint, jsonify

tep_bp = Blueprint('tep', __name__)

@tep_bp.route('/tep/<int:id>', methods=['GET'])
def api_get_tep(id):
    # importe aquí para evitar importaciones circulares
    from crud.tep_crud import get_tep_by_id
    tep = get_tep_by_id(id)
    if not tep:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(tep.dict()), 200