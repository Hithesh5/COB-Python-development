import requests
from flask import Flask, render_template, request

app = Flask(__name__)

SPOONACULAR_API_KEY = '60fd8ed1ea2c4374867383d943852923'
SEARCH_API_URL = 'https://api.spoonacular.com/recipes/findByIngredients'
RECIPE_API_URL = 'https://api.spoonacular.com/recipes'


def get_recipes_by_ingredients(ingredients):
    params = {
        'ingredients': ','.join(ingredients),
        'apiKey': SPOONACULAR_API_KEY,
    }

    try:
        response = requests.get(SEARCH_API_URL, params=params)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        recipes = response.json()
        return recipes
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None


def get_recipe_details(recipe_id):
    params = {
        'apiKey': SPOONACULAR_API_KEY,
    }

    try:
        response = requests.get(f'{RECIPE_API_URL}/{recipe_id}/information', params=params)
        response.raise_for_status()

        recipe_details = response.json()
        return recipe_details
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    ingredients = request.form.get('ingredients')
    ingredients_list = ingredients.split(',')

    # Get recipes based on ingredients
    recipes = get_recipes_by_ingredients(ingredients_list)

    if recipes:
        results = []
        for i, recipe in enumerate(recipes, start=1):
            result = {
                'title': recipe['title'],
                'missed_ingredients': [missed.get('name', '') for missed in recipe.get('missedIngredients', [])],
                'used_ingredients': [used.get('name', '') for used in recipe.get('usedIngredients', [])],
                'likes': recipe.get('likes', 'N/A')
            }

            # Get additional details for each recipe
            recipe_details = get_recipe_details(recipe['id'])
            if recipe_details:
                result['instructions'] = recipe_details.get('instructions', 'N/A')
            else:
                result['instructions'] = "Failed to fetch additional details for this recipe."

            results.append(result)

        return render_template('result.html', results=results)
    else:
        return "Error fetching recipes"


if __name__ == '__main__':
    app.run(debug=True)
