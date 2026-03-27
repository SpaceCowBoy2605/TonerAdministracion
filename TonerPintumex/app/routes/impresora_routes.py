from flask import Blueprint, jsonify

imporesora_bp = Blueprint('Imporesora', __name__)


def _dump_impresora(model):
    """Serializa una impresora evitando duplicar ids cuando hay objetos anidados."""
    if hasattr(model, "model_dump"):
        data = model.model_dump()
    else:
        data = model.dict()

    # Si viene el objeto anidado, no repetir el FK a nivel raíz
    if data.get("accesorio") is not None:
        data.pop("idAccesorio", None)
    if data.get("cedis") is not None:
        data.pop("idCedis", None)
    if data.get("planta") is not None:
        data.pop("idPlanta", None)
    if data.get("resu") is not None:
        data.pop("idResu", None)
    if data.get("tep") is not None:
        data.pop("idTep", None)

    # Opcional: si el FK es null, no lo mandes
    for k in ("idAccesorio", "idCedis", "idPlanta", "idResu", "idTep"):
        if data.get(k) is None:
            data.pop(k, None)

    return data

@imporesora_bp.route('/impresora', methods=['GET'])
def api_get_all_impresoras():

    from app.crud.impresora_crud import get_all_impresora
    impresoras = get_all_impresora()
    if not impresoras:
        return jsonify([]), 200
    return jsonify([_dump_impresora(impresora) for impresora in impresoras]), 200


@imporesora_bp.route('/impresora/<int:id>', methods=['GET'])
def api_get_impresora(id):
    # importe aquí para evitar importaciones circulares
    from app.crud.impresora_crud import get_impresora_by_id
    Impresora = get_impresora_by_id(id)
    if not Impresora:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(_dump_impresora(Impresora)), 200

@imporesora_bp.route('/impresora/crear', methods=['POST'])
def api_create_impresora():

    from app.crud.impresora_crud import create_impresora
    from flask import request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos inválidos"}), 400
    impresora = create_impresora(data)
    return jsonify({"message": "Impresora creada", "impresora": impresora}), 200

@imporesora_bp.route('/impresora/actualizar/<int:id>', methods=['PUT'])
def api_update_impresora(id):

    from app.crud.impresora_crud import update_impresora
    from flask import request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos inválidos"}), 400
    success = update_impresora(id, data)
    if not success:
        return jsonify({"error": "Impresora no encontrada"}), 404
    return jsonify({"message": "Impresora actualizada"}), 200


@imporesora_bp.route('/impresora/eliminar/<int:id>', methods=['DELETE'])
def api_delete_impresora(id):

    from app.crud.impresora_crud import delete_impresora
    success = delete_impresora(id)
    if not success:
        return jsonify({"error": "Impresora no encontrada"}), 404
    return jsonify({"message": "Impresora eliminada"}), 200

