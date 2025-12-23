from flask import Blueprint, jsonify

accesorio_bp = Blueprint('accesorio', __name__)

@accesorio_bp.route('/accesorio/<int:id>', methods=['GET'])
def api_get_accesorio(id):
    # importe aquí para evitar importaciones circulares
    from crud.accesorio_crud import get_accesorio_by_id
    accesorio = get_accesorio_by_id(id)
    if not accesorio:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(accesorio.dict()), 200