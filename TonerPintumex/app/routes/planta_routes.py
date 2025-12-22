from flask import Blueprint, jsonify

planta_bp = Blueprint('planta', __name__)


@planta_bp.route('/planta/<int:id>', methods=['GET'])
def api_get_planta(id):
	# importe aquí para evitar importaciones circulares
	from crud.planta_crud import get_planta_by_id
	planta = get_planta_by_id(id)
	if not planta:
		return jsonify({'error': 'No encontrado'}), 404
	return jsonify(planta.dict()), 200

