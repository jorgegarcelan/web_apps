import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Recipes.model import Recipe, Ingredient, QuantifiedIngredient, Step, Rating, Photo  # import your models
from Recipes.__init__ import db, create_app
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = create_app()

def import_csv_data():
    with app.app_context():
        # Read the CSV files
        df_recipes = pd.read_csv('data/recipes.csv')
        df_ingredients = pd.read_csv('data/ingredients.csv')
        df_quantified_ingredients = pd.read_csv('data/quantified_ingredients.csv')
        df_steps = pd.read_csv('data/steps.csv')
        df_ratings = pd.read_csv('data/ratings.csv')
        df_photos = pd.read_csv('data/photos.csv')

        # Import data into the database
        for _, row in df_recipes.iterrows():
            db.session.add(Recipe(**row.to_dict()))
            # After each commit, log the result
            logging.info("Imported data into the database successfully.")
        
        for _, row in df_ingredients.iterrows():
            db.session.add(Ingredient(**row.to_dict()))
            # After each commit, log the result
            logging.info("Imported data into the database successfully.")
        
        for _, row in df_quantified_ingredients.iterrows():
            db.session.add(QuantifiedIngredient(**row.to_dict()))
            # After each commit, log the result
            logging.info("Imported data into the database successfully.")
        
        for _, row in df_steps.iterrows():
            db.session.add(Step(**row.to_dict()))
            # After each commit, log the result
            logging.info("Imported data into the database successfully.")
        
        for _, row in df_ratings.iterrows():
            db.session.add(Rating(**row.to_dict()))
            # After each commit, log the result
            logging.info("Imported data into the database successfully.")
        
        for _, row in df_photos.iterrows():
            db.session.add(Photo(**row.to_dict()))
            # After each commit, log the result
            logging.info("Imported data into the database successfully.")

        # Commit all changes
        db.session.commit()

if __name__ == '__main__':
    import_csv_data()