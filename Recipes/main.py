import datetime
import dateutil.tz
from flask import Blueprint, render_template, abort, request, url_for, flash, redirect
from flask_login import current_user, login_required
from sqlalchemy.sql import func
from . import model
from Recipes import db, create_app, gpt
from werkzeug.utils import secure_filename
import os
import numpy as np

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    top_recipes = db.session.query(
        model.Recipe, 
        func.avg(model.Rating.value).label('average_rating')
    ).join(model.Rating).group_by(model.Recipe.id).order_by(func.avg(model.Rating.value).desc()).limit(5).all()

    return render_template('main/main.html', top_recipes=top_recipes)


@bp.route("/user/<int:user_id>")
def user(user_id):
    # user:
    query_u = db.select(model.User).where(model.User.id == user_id)
    user = db.session.execute(query_u).scalar_one_or_none()
    print(user)
    
    # recipes:
    query_r = db.select(model.Recipe).where(model.Recipe.user_id == user_id)
    recipes = db.session.execute(query_r).scalars().all()
    print(recipes)

    if not recipes:
        abort(404, "Recipes for User id {} doesn't exist.".format(user_id))

    # photos:
    query_p = db.select(model.Photo).where(model.Photo.user_id == user_id)
    photos = db.session.execute(query_p).scalars().all()
    print(photos)
    
    return render_template("user/user.html", user=user, recipes=recipes, photos=photos)


@bp.route("/recipes/<int:recipe_id>")
def recipe(recipe_id):
    # recipe:
    query_r = db.select(model.Recipe).where(model.Recipe.id == recipe_id)
    recipe = db.session.execute(query_r).scalar_one_or_none()
    print(recipe)
    
    # user:
    query_u = db.select(model.User).where(model.User.id == recipe.user_id)
    user = db.session.execute(query_u).scalar_one_or_none()
    print(user)

    # rating:
    query_rt = db.select(model.Rating.value).where(model.Rating.recipe_id == recipe_id)
    ratings_list = db.session.execute(query_rt).scalars().all()
    count = len(ratings_list)

    # ingredients:
    print(recipe.quantified_ingredients)
    quantified_ingredients = model.QuantifiedIngredient.query.filter_by(recipe_id=recipe_id).all()     # Query the QuantifiedIngredient model to get all entries related to the recipe_id

    ingredients_info = []
    for qi in quantified_ingredients:
        ingredient_detail = {
            'name': qi.ingredient.name,
            'quantity': qi.quantity,
            'unit_of_measurement': qi.unit_of_measurement
        }
        ingredients_info.append(ingredient_detail)

    # bookmark:
    bookmark = model.Bookmark.query.filter_by(user_id=user.id, recipe_id=recipe_id).first()      # Query to check if the current user has bookmarked the recipe
    is_bookmarked = bookmark is not None

    # ratings:
    if count == 0:
        rating = "No reviews yet"
        return render_template("recipes/recipes.html", recipe=recipe, user=user, rating=rating, ingredients_info=ingredients_info, is_bookmarked=is_bookmarked)

    else:
        count = f"({count})"
        rating = round(np.mean(ratings_list), 1)
        rating = str(rating) + " / 5"
        return render_template("recipes/recipes.html", recipe=recipe, user=user, rating=rating, count=count, ingredients_info=ingredients_info, is_bookmarked=is_bookmarked)


@bp.route('/bookmark/<int:recipe_id>', methods=['POST'])
def bookmark_recipe(recipe_id):
    # Check if bookmark already exists
    bookmark = model.Bookmark.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
    if bookmark:
        # Bookmark exists, remove it
        db.session.delete(bookmark)
        db.session.commit()
        flash('Bookmark removed.')
    else:
        # Bookmark does not exist, add a new one
        new_bookmark = model.Bookmark(user_id=current_user.id, recipe_id=recipe_id)
        db.session.add(new_bookmark)
        db.session.commit()
        flash('Recipe bookmarked.')

    return redirect(url_for('main.recipe', recipe_id=recipe_id))


@bp.route("/recipe_vision", methods=['GET', 'POST'])
def recipe_vision():
    if request.method == 'POST':
        file = request.files.get('file')

        if not file or file.filename == '':
            return 'No selected file'

        # Save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join('Recipes/static/imgs', filename)
        print(filename)
        file.save(filepath)
        print(filepath)

        # Process the image with your GPT model here
        output = gpt.gpt4_vision(filepath)

        # URL for the uploaded image
        uploaded_image_url = url_for('static', filename='imgs/' + filename)

        return render_template("gpt/gpt4vision.html", output=output, uploaded_image=uploaded_image_url)

    return render_template("gpt/gpt4vision.html")