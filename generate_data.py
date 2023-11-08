# Generate new data for the CSV files with 25 entries for each table

import random
import string
import pandas as pd

# Helper function to create a random string (for titles, descriptions, etc.)
def random_string(length=10):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

# Recipes data
recipes_data = {
    'id': list(range(1, 26)),
    'title': [random_string(10) for _ in range(25)],
    'description': [random_string(50) for _ in range(25)],
    'user_id': [random.randint(1, 10) for _ in range(25)],
    'servings': [random.randint(1, 10) for _ in range(25)],
    'cook_time': [random.randint(10, 120) for _ in range(25)]
}

# Ingredients data
ingredients_data = {
    'id': list(range(1, 26)),
    'name': [random_string(10) for _ in range(25)]
}

# QuantifiedIngredients data
quantified_ingredients_data = {
    'id': list(range(1, 26)),
    'ingredient_id': [random.randint(1, 25) for _ in range(25)],
    'recipe_id': [random.randint(1, 25) for _ in range(25)],
    'quantity': [str(random.randint(1, 10)) for _ in range(25)],
    'unit_of_measurement': [random.choice(['g', 'ml', 'cups', 'tbsp', 'tsp']) for _ in range(25)]
}

# Steps data
steps_data = {
    'id': list(range(1, 26)),
    'recipe_id': [random.randint(1, 25) for _ in range(25)],
    'sequence_number': list(range(1, 26)),
    'description': [random_string(50) for _ in range(25)]
}

# Ratings data
ratings_data = {
    'id': list(range(1, 26)),
    'user_id': [random.randint(1, 10) for _ in range(25)],
    'recipe_id': [random.randint(1, 25) for _ in range(25)],
    'value': [random.randint(1, 5) for _ in range(25)]
}

# Photos data
photos_data = {
    'id': list(range(1, 26)),
    'user_id': [random.randint(1, 10) for _ in range(25)],
    'recipe_id': [random.randint(1, 25) for _ in range(25)],
    'file_extension': [random.choice(['.jpg', '.png', '.jpeg']) for _ in range(25)]
}

# Convert the dictionaries to pandas DataFrames
df_recipes = pd.DataFrame(recipes_data)
df_ingredients = pd.DataFrame(ingredients_data)
df_quantified_ingredients = pd.DataFrame(quantified_ingredients_data)
df_steps = pd.DataFrame(steps_data)
df_ratings = pd.DataFrame(ratings_data)
df_photos = pd.DataFrame(photos_data)

# Save each DataFrame to a CSV file
df_recipes.to_csv('data/recipes.csv', index=False)
df_ingredients.to_csv('data/ingredients.csv', index=False)
df_quantified_ingredients.to_csv('data/quantified_ingredients.csv', index=False)
df_steps.to_csv('data/steps.csv', index=False)
df_ratings.to_csv('data/ratings.csv', index=False)
df_photos.to_csv('data/photos.csv', index=False)

# File paths for the user
file_paths = {
    'recipes': 'data/recipes.csv',
    'ingredients': 'data/ingredients.csv',
    'quantified_ingredients': 'data/quantified_ingredients.csv',
    'steps': 'data/steps.csv',
    'ratings': 'data/ratings.csv',
    'photos': 'data/photos.csv'
}
