import json
import requests


def lambda_handler(event, context):
    # Get the Pokémon name from the URL
    params = event.get("queryStringParameters") or {}
    pokemon_name = params.get("pokemon")

    # Make sure a Pokémon name was provided
    if not pokemon_name:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "STUDENT TODO: Write a useful error message"}),
        }

    pokemon_name = pokemon_name.lower().strip()

    # Ask PokéAPI for information about this Pokémon
    response = requests.get(
        f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}",
        timeout=5,
    )

    # What should our application return if the Pokémon doesn't exist?
    if response.status_code == 404:
        # STUDENT TODO
        return {}

    # Handle other unexpected errors from PokéAPI
    if not response.ok:
        return {
            "statusCode": 502,
            "body": json.dumps({"error": "PokéAPI returned an unexpected response."}),
        }

    data = response.json()

    # Pull information from the PokéAPI response.
    # These are examples. Explore the response and decide what
    # information your application needs.
    name = data["name"].title()
    weight = data["weight"]

    # STUDENT TODO:
    # Use the Pokémon data to make your own decision,
    # calculation, or classification.
    decision = "STUDENT TODO"

    # STUDENT TODO:
    # Include the information needed to explain your result.
    result = {
        "pokemon": name,
        "weight": weight,
        "decision": decision,
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(result),
    }
