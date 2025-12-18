from flask import Flask, jsonify, request


app= Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/api/planta/<int:id>', methods=['GET'])
def api_get_planta(id):
    # importe aquí para evitar importaciones circulares
    from crud.planta_crud import get_planta_by_id
    planta = get_planta_by_id(id)
    if not planta:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(planta.dict()), 200

if __name__ == '__main__':
    app.run() 