from flask import Blueprint, jsonify

factura_bp = Blueprint('Factura', __name__)

@factura_bp.route('/factura/<int:id>', methods=['GET'])
def api_get_factura(id):
    # importe aquí para evitar importaciones circulares
    from app.crud.factura_crud import get_factura_by_id
    Factura = get_factura_by_id(id)
    if not Factura:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(Factura.dict()), 200

@factura_bp.route('/factura', methods=['GET'])
def api_get_all_factura():
    # importe aquí para evitar importaciones circulares
    from app.crud.factura_crud import get_all_factura
    Factura_list = get_all_factura()
    if not Factura_list:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify([factura.dict() for factura in Factura_list]), 200


@factura_bp.route('/factura/crear', methods=['POST'])
def api_create_factura():
    from flask import request
    from app.crud.factura_crud import create_factura

    data = request.get_json()
    new_factura = create_factura(data)
    if not new_factura:
        return jsonify({'error': 'No se pudo crear'}), 400
    return jsonify(new_factura.dict()), 201