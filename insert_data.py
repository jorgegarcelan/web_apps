import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Recipes.model import User, Recipe, Ingredient, QuantifiedIngredient, Step, Rating, Bookmark, Photo  # import your models
from Recipes import db, create_app
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = create_app()

def import_csv_data():
    with app.app_context():
        # Read the CSV files
        df_users = pd.read_csv('data/users.csv', sep=";")
        df_recipes = pd.read_csv('data/recipes.csv', sep=";")
        df_ingredients = pd.read_csv('data/ingredients.csv', sep=";")
        df_quantified_ingredients = pd.read_csv('data/quantified_ingredients.csv', sep=";")
        df_steps = pd.read_csv('data/steps.csv', sep=";")
        df_ratings = pd.read_csv('data/ratings.csv', sep=";")
        df_bookmark = pd.read_csv('data/bookmark.csv', sep=";")
        #df_photos = pd.read_csv('data/photos.csv')

        # Import data into the database
        for _, row in df_users.iterrows():
            new_user = User(email=row['email'], name=row['name'], username=row['username'])
            new_user.set_password(row['password'])
            db.session.add(new_user)

            # Log the result
            logging.info("Imported users into the database successfully.")

        for _, row in df_recipes.iterrows():
            db.session.add(Recipe(**row.to_dict()))
            # Log the result
            logging.info("Imported recipes into the database successfully.")
        
        for _, row in df_ingredients.iterrows():
            db.session.add(Ingredient(**row.to_dict()))
            # Log the result
            logging.info("Imported ingredients into the database successfully.")
        
        for _, row in df_quantified_ingredients.iterrows():
            db.session.add(QuantifiedIngredient(**row.to_dict()))
            # Log the result
            logging.info("Imported quantified_ingredients into the database successfully.")
        
        for _, row in df_steps.iterrows():
            db.session.add(Step(**row.to_dict()))
            # Log the result
            logging.info("Imported steps into the database successfully.")
        
        for _, row in df_ratings.iterrows():
            db.session.add(Rating(**row.to_dict()))
            # Log the result
            logging.info("Imported ratings into the database successfully.")

        for _, row in df_bookmark.iterrows():
            db.session.add(Bookmark(**row.to_dict()))
            # Log the result
            logging.info("Imported bookmark into the database successfully.")
        
        """
        for _, row in df_photos.iterrows():
            db.session.add(Photo(**row.to_dict()))
            # After each commit, log the result
            logging.info("Imported data into the database successfully.")
        """
        

        # Commit all changes
        db.session.commit()

if __name__ == '__main__':
    import_csv_data()