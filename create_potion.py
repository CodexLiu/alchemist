from typing import Dict, Any
import json
from chat_service import get_chat_response
from db_service import get_cached_potion, cache_potion


def get_ingredients_match_incantation(ingredients, incantation):
    determine_ingredients_match_incantation_prompt = f"""Determine how well the ingredients {ingredients} are reasonably suitable to achieve the desired effect {incantation} in a very whimsical RPG game.
    Return an integer value from 0 to 10 based on the following criteria:
    0 - Ingredients have no relation to the incantation and cannot achieve the desired effect.
    1-2 - Ingredients have minimal relation to the incantation and are highly unlikely to achieve the desired effect.
    3-4 - Ingredients have some relation to the incantation but are not very effective in achieving the desired effect.
    5-6 - Ingredients are moderately related to the incantation and can achieve the desired effect to some extent.
    7-8 - Ingredients are closely related to the incantation and can achieve the desired effect effectively.
    9-10 - Ingredients are perfectly related to the incantation and can achieve the desired effect with high precision.
    Do not return any other text.
    """
    determine_ingredients_match_incantation_response = get_chat_response(
        determine_ingredients_match_incantation_prompt)
    # Convert string response to integer
    return int(determine_ingredients_match_incantation_response.strip())


# get the name of the potion
def get_potion_name(ingredients, incantation, ingredients_match_incantation):
    name_prompt = f"""Give me the name of the potion that is made of {ingredients} and has the following incantation said while it was being made {incantation}. The effectiveness of the potion out of 10 is {ingredients_match_incantation}. the name should match the effectiveness of the potion.
Give your answer in the form of "Potion of <name>". limit <name> to 3 words maximum. The name should reference both the ingredients and the incantation.
"""
    name_response = get_chat_response(name_prompt)
    return name_response


# get color of the potion
def get_potion_color(ingredients, incantation, potion_name):
    color_prompt = f"""Give me the color of the potion that is made of {ingredients}. The name of the potion is {potion_name}. Return only the color of the potion using hex code and nothing else. 
"""
    color_response = get_chat_response(color_prompt)
    return color_response


# get the effect of the potion
def parse_effect_response(response: str) -> Dict[str, Any]:
    try:
        cleaned_response = response.replace(
            '```json', '').replace('```', '').strip()
        return json.loads(cleaned_response)
    except json.JSONDecodeError:
        # Default effect if parsing fails
        return {
            "size": None,
            "position": None,
            "health": None,
            "jump_velocity": None,
            "speed": None,
            "duration": None
        }


def get_potion_effect(ingredients: str, incantation: str, potion_name: str, ingredients_match_incantation: int) -> Dict[str, Any]:
    effect_prompt = f"""Analyze this magical potion and provide its effects:
    
    Potion Name: {potion_name}
    Ingredients: {ingredients}
    Incantation: {incantation}
    Potion Effectiveness out of 10: {ingredients_match_incantation}
    
    The most important thing to consider is the effectiveness of the potion out of 10. With a value closer to 0 the effect will be minimal and with a value closer to 10 the effect will be extreme.
    
    Determine the impact on each parameter:

    1. Size: Decimal multiplier (e.g., 0.5 for half size, 2.0 for double, 1 being normal)
    2. Position: Tuple of (delta_x, delta_y), teleports the object to a new position the units is in inches
    3. Health: sets the health of the object to the minimum of 0 and the maximum of 10
    4. Jump Velocity: Decimal multiplier (e.g., 0.5 for half jump, 1.5 for enhanced, 1 being normal)
    5. Speed: Decimal multiplier (e.g., 0.5 for half speed, 1.5 for enhanced, 1 being normal)
    6. Duration: Effect duration in seconds
    
    Return ONLY a valid JSON object with these exact keys:
    {{
        "size": <decimal or null>,
        "position": <[x,y] or null>,
        "health": <int or null>,
        "jump_velocity": <decimal or null>,
        "speed": <decimal or null>,
        "duration": <int or null>
    }}
    """

    try:
        effect_response = get_chat_response(effect_prompt)

        effects = parse_effect_response(effect_response)

        required_keys = ["size", "position", "health",
                         "jump_velocity", "speed", "duration"]
        for key in required_keys:
            if key not in effects:
                effects[key] = None

        return effects

    except Exception as e:
        print(f"Error generating potion effect: {str(e)}")
        # Return default effect in case of any error
        return {
            "size": None,
            "position": None,
            "health": None,
            "jump_velocity": None,
            "speed": None,
            "duration": None
        }


def create_potion(ingredients, incantation):
    # First, check if we have this potion cached
    cached_result = get_cached_potion(ingredients, incantation)
    if cached_result:
        return cached_result

    # If not cached, generate the potion details
    ingredients_match_incantation = get_ingredients_match_incantation(
        ingredients, incantation)
    potion_name = get_potion_name(
        ingredients, incantation, ingredients_match_incantation)
    potion_color = get_potion_color(ingredients, incantation, potion_name)
    potion_effect = get_potion_effect(
        ingredients, incantation, potion_name, ingredients_match_incantation)

    potion_details = {
        "ingredients": ingredients,
        "incantation": incantation,
        "effectiveness": ingredients_match_incantation,
        "potion_name": potion_name,
        "potion_color": potion_color,
        "potion_effect": potion_effect
    }

    # Cache the result for future use
    cache_potion(potion_details)

    return potion_details


def main():
    ingredients = ["dirt", "mushroom"]
    incantation = "make me fly"
    potion_details = create_potion(ingredients, incantation)
    print(potion_details)


if __name__ == "__main__":
    main()
