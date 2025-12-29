from flask import Blueprint, jsonify

imporesora_bp = Blueprint('Imporesora', __name__)

@imporesora_bp.route('/impresora/<int:id>', methods=['GET'])
def api_get_impresora(id):
    # importe aquí para evitar importaciones circulares
    from crud.impresora_crud import get_impresora_by_id
    Impresora = get_impresora_by_id(id)
    if not Impresora:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(Impresora.dict()), 200
