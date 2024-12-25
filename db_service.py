import sqlite3
import json


def init_db():
    conn = sqlite3.connect('potions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS potions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredients TEXT NOT NULL,
            incantation TEXT NOT NULL,
            effectiveness INTEGER NOT NULL,
            potion_name TEXT NOT NULL,
            potion_color TEXT NOT NULL,
            potion_effect TEXT NOT NULL,
            UNIQUE(ingredients, incantation)
        )
    ''')
    conn.commit()
    conn.close()


def get_cached_potion(ingredients, incantation):
    conn = sqlite3.connect('potions.db')
    c = conn.cursor()

    # Convert ingredients list to a sorted string representation for consistent matching
    ingredients_str = json.dumps(sorted(ingredients))

    c.execute('SELECT * FROM potions WHERE ingredients = ? AND incantation = ?',
              (ingredients_str, incantation))
    result = c.fetchone()
    conn.close()

    if result:
        return {
            'ingredients': json.loads(result[1]),
            'incantation': result[2],
            'effectiveness': result[3],
            'potion_name': result[4],
            'potion_color': result[5],
            'potion_effect': json.loads(result[6])
        }
    return None


def cache_potion(potion_details):
    conn = sqlite3.connect('potions.db')
    c = conn.cursor()

    # Convert ingredients list to a sorted string representation
    ingredients_str = json.dumps(sorted(potion_details['ingredients']))

    try:
        c.execute('''
            INSERT INTO potions 
            (ingredients, incantation, effectiveness, potion_name, potion_color, potion_effect)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            ingredients_str,
            potion_details['incantation'],
            potion_details['effectiveness'],
            potion_details['potion_name'],
            potion_details['potion_color'],
            json.dumps(potion_details['potion_effect'])
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        # If the potion already exists, we'll just skip inserting
        pass
    finally:
        conn.close()


# Initialize the database when the module is imported
init_db()
