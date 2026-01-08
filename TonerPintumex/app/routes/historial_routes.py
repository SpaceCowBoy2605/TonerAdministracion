from flask import Blueprint, jsonify

historial_bp = Blueprint('historial', __name__)

@historial_bp.route('/historial', methods=['GET'])
def api_get_all_historial():
    # importe aquí para evitar importaciones circulares
    from crud.historial_crud import get_all_historial
    historiales = get_all_historial()
    if not historiales:
        return jsonify([]), 200
    return jsonify([historial.dict() for historial in historiales]), 200

@historial_bp.route('/historial/<int:id>', methods=['GET'])
def api_get_historial(id):
    # importe aquí para evitar importaciones circulares
    from crud.historial_crud import get_historial_by_id
    historial = get_historial_by_id(id)
    if not historial:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(historial.dict()), 200