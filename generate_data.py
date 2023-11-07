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
df_recipes_new = pd.DataFrame(recipes_data)
df_ingredients_new = pd.DataFrame(ingredients_data)
df_quantified_ingredients_new = pd.DataFrame(quantified_ingredients_data)
df_steps_new = pd.DataFrame(steps_data)
df_ratings_new = pd.DataFrame(ratings_data)
df_photos_new = pd.DataFrame(photos_data)

# Save each DataFrame to a CSV file
df_recipes_new.to_csv('/data/recipes_new.csv', index=False)
df_ingredients_new.to_csv('/data/ingredients_new.csv', index=False)
df_quantified_ingredients_new.to_csv('/data/quantified_ingredients_new.csv', index=False)
df_steps_new.to_csv('/data/steps_new.csv', index=False)
df_ratings_new.to_csv('/data/ratings_new.csv', index=False)
df_photos_new.to_csv('/data/photos_new.csv', index=False)

# File paths for the user
file_paths_new = {
    'recipes': '/data/recipes_new.csv',
    'ingredients': '/data/ingredients_new.csv',
    'quantified_ingredients': '/data/quantified_ingredients_new.csv',
    'steps': '/data/steps_new.csv',
    'ratings': '/data/ratings_new.csv',
    'photos': '/data/photos_new.csv'
}
