from flask import Blueprint, jsonify

planta_bp = Blueprint('planta', __name__)

#metoddos get
@planta_bp.route('/planta', methods=['GET'])
def api_get_all_plantas():

	from crud.planta_crud import get_all_planta
	plantas = get_all_planta()
	if not plantas:
		return jsonify([]), 200
	return jsonify([planta.dict() for planta in plantas]), 200

@planta_bp.route('/planta/<int:id>', methods=['GET'])
def api_get_planta(id):

	from crud.planta_crud import get_planta_by_id
	planta = get_planta_by_id(id)
	if not planta:
		return jsonify({'error': 'No encontrado'}), 404
	return jsonify(planta.dict()), 200

#metoddos post
@planta_bp.route('/planta/crear', methods=['POST'])
def api_create_planta():

	from crud.planta_crud import create_planta
	from flask import request
	data = request.get_json()
	if not data:
		return jsonify({"error": "Datos inválidos"}), 400
	planta = create_planta(data)
	return jsonify({"message": "Departamento de planta creado", "planta": planta}), 200

#metoddos put
@planta_bp.route('/planta/actualizar/<int:id>', methods=['PUT'])
def api_update_planta(id):

	from crud.planta_crud import update_planta
	from flask import request
	data = request.get_json()
	if not data:
		return jsonify({"error": "Datos inválidos"}), 400
	updated_planta = update_planta(id, data)
	if not updated_planta:
		return jsonify({"error": "No encontrado"}), 404
	return jsonify({"message": "Departamento de planta actualizado"}), 200

#metoddos delete
@planta_bp.route('/planta/eliminar/<int:id>', methods=['DELETE'])
def api_delete_planta(id):

	from crud.planta_crud import delete_planta
	deleted_planta = delete_planta(id)
	if not deleted_planta:
		return jsonify({"error": "Departamento no encontrado"}), 404
	return jsonify({"message": "Departamento de planta eliminado"}), 200