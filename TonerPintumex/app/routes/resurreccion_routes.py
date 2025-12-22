from flask import Blueprint, jsonify

resurreccion_bp = Blueprint('resurreccion', __name__)


@resurreccion_bp.route('/resurreccion/<int:id>', methods=['GET'])
def api_get_resurreccion(id):
    # importe aquí para evitar importaciones circulares
    from crud.resurrecion_crud import get_resurrecion_by_id
    resurreccion = get_resurrecion_by_id(id)
    if not resurreccion:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(resurreccion.dict()), 200
