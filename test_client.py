import requests
import json


def test_potion_creation():
    # Server URL
    url = 'http://localhost:5000/chat'

    # Test cases
    test_cases = [
        {
            "ingredients": ["mushroom", "fairy dust"],
            "incantation": "make me fly high"
        },
        {
            "ingredients": ["toad", "snake venom", "spider web"],
            "incantation": "curse my enemies"
        },
        {
            "ingredients": ["honey", "rainbow essence"],
            "incantation": "heal my wounds"
        }
    ]

    # Test each case
    for i, test_data in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Sending request with: {json.dumps(test_data, indent=2)}")

        try:
            # Send POST request
            response = requests.post(url, json=test_data)

            # Check if request was successful
            if response.status_code == 200:
                print("\nSuccess! Potion created:")
                print(json.dumps(response.json(), indent=2))
            else:
                print(f"\nError: Status code {response.status_code}")
                print(f"Response: {response.text}")

        except requests.exceptions.ConnectionError:
            print(
                "\nError: Could not connect to server. Make sure the server is running on localhost:5000")
        except Exception as e:
            print(f"\nError: {str(e)}")

        print("\n" + "="*50)


if __name__ == "__main__":
    test_potion_creation()
