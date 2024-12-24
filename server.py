from flask import Flask, request, jsonify
from flask_cors import CORS
from chat_service import get_chat_response
from create_potion import create_potion  # Add this import

app = Flask(__name__)
CORS(app)


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        ingredients = data.get('ingredients', [])
        incantation = data.get('incantation', '')

        # Call create_potion with the ingredients and incantation
        potion_details = create_potion(ingredients, incantation)
        return jsonify(potion_details)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
