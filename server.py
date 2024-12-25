from flask import Flask, request, jsonify
from flask_cors import CORS
from chat_service import get_chat_response
from create_potion import create_potion  # Add this import

app = Flask(__name__)
CORS(app)


@app.route('/chat', methods=['POST'])
def chat():
    try:
        print("Request received")
        data = request.json
        ingredients = data.get('ingredients', [])
        incantation = data.get('incantation', '')

        # Calculate total power by summing the power values from ingredients
        total_power = 1.0  # Default power
        if ingredients and isinstance(ingredients[0], dict):
            total_power = sum(ingredient.get('power', 0)
                              for ingredient in ingredients)
            if total_power == 0:  # Fallback to 1.0 if no powers found
                total_power = 1.0
            # Extract just the ingredient names for the potion creation
            ingredients = [ingredient.get('name', str(ingredient))
                           for ingredient in ingredients]

        # Call create_potion with the ingredients and incantation
        potion_details = create_potion(ingredients, incantation)

        # Ensure effect values are never null
        effects = potion_details['potion_effect']
        effects['size'] = effects['size'] if effects['size'] is not None else 1.0
        effects['speed'] = effects['speed'] if effects['speed'] is not None else 1.0
        effects['jump_velocity'] = effects['jump_velocity'] if effects['jump_velocity'] is not None else 1.0
        effects['health'] = effects['health'] if effects['health'] is not None else 0
        effects['duration'] = effects['duration'] if effects['duration'] is not None else 10
        effects['position'] = effects['position'] if effects['position'] is not None else [
            0, 0]

        # Add the calculated total_power to the response
        potion_details['total_power'] = total_power

        print("Data sent:", potion_details)
        return jsonify(potion_details)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
