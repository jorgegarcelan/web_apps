import datetime
import dateutil.tz
from flask import Blueprint, render_template, abort, request, url_for, flash, redirect, current_app
from flask_login import current_user, login_required
from sqlalchemy.sql import func
from . import model
from Recipes import db, create_app, gpt
from werkzeug.utils import secure_filename
import os
import numpy as np
import pathlib

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
    bookmark = model.Bookmark.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()      # Query to check if the current user has bookmarked the recipe
    is_bookmarked = bookmark is not None

    # photos:
    chef_photos = model.Photo.query.filter_by(user_id=user.id, recipe_id=recipe_id).all()
    print(chef_photos)

    # ratings:
    rate = model.Rating.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()      # Query to check if the current user has bookmarked the recipe
    is_rated = rate is not None

    query_rt = db.select(model.Rating.value).where(model.Rating.recipe_id == recipe_id)
    ratings_list = db.session.execute(query_rt).scalars().all()
    count = len(ratings_list)

    if is_rated == False:
        return render_template("recipes/recipes.html", recipe=recipe, user=user, rating=rating, ingredients_info=ingredients_info, is_bookmarked=is_bookmarked, is_rated=is_rated, chef_photos=chef_photos)

    if count == 0:
        rating = "No reviews yet"
        return render_template("recipes/recipes.html", recipe=recipe, user=user, rating=rating, ingredients_info=ingredients_info, is_bookmarked=is_bookmarked, is_rated=is_rated, chef_photos=chef_photos)

    else:
        count = f"({count})"
        rating = round(np.mean(ratings_list), 1)
        rating = str(rating) + " / 5"
        return render_template("recipes/recipes.html", recipe=recipe, user=user, rating=rating, current_rate=rate.value, count=count, ingredients_info=ingredients_info, is_bookmarked=is_bookmarked, is_rated=is_rated, chef_photos=chef_photos)


@bp.route('/edit_recipe', methods=['POST'])
def edit_recipe():
    # Get data from the submitted form
    recipe_id = request.form.get('recipe_id')
    name = request.form.get('edit_name')
    description = request.form.get('edit_description')
    servings = request.form.get('edit_servings')
    cook_time = request.form.get('edit_cook_time')
    type_food = request.form.get('edit_type_food')
    category_food = request.form.get('edit_category_food')

    print(f"{recipe_id=}")
    print(f"{name=}")
    print(f"{description=}")
    print(f"{servings=}")
    print(f"{cook_time=}")
    print(f"{type_food=}")
    print(f"{category_food=}")

    recipe = model.Recipe.query.get_or_404(recipe_id)

    # Update the recipe with the new data
    recipe.title = name
    recipe.description = description
    recipe.servings = int(servings) if servings.isdigit() else None
    recipe.cook_time = int(cook_time) if cook_time.isdigit() else None
    recipe.type_food = type_food
    recipe.category_food = category_food

    # Commit the changes to the database
    db.session.commit()

    flash('Recipe updated successfully!', 'success')

    return redirect(url_for('main.recipe', recipe_id=recipe_id))


@bp.route('/bookmark', methods=['POST'])
def bookmark_recipe():
    # Get data from the submitted form
    recipe_id = request.form.get('recipe_id')

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


@bp.route('/rate_recipe', methods=['POST'])
def rate_recipe():
    # Get data from the submitted form
    rating_value = request.form.get('rating')
    recipe_id = request.form.get('recipe_id')

    # Check if the rating already exists for the user and recipe
    rating = model.Rating.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()

    if rating:
        # If a rating exists, update it
        rating.value = rating_value
        flash('Your rating has been updated.')
    else:
        # If no rating exists, create a new one
        new_rating = model.Rating(user_id=current_user.id, recipe_id=recipe_id, value=rating_value)
        db.session.add(new_rating)
        flash('Your rating has been recorded.')

    db.session.commit()

    # Redirect to the recipe page or wherever is appropriate
    return redirect(url_for('main.recipe', recipe_id=recipe_id))


@bp.route('/upload_image', methods=['POST'])
def upload_photo():
    # Get data from form
    uploaded_file = request.files['file']
    recipe_id = request.form.get('recipe_id')

    if uploaded_file.filename != '':
        content_type = uploaded_file.content_type
        if content_type == "image/png":
            file_extension = "png"
        elif content_type == "image/jpeg":
            file_extension = "jpg"
        else:
            abort(400, f"Unsupported file type {content_type}")

        # Fetch the recipe from the database
        recipe = model.Recipe.query.get_or_404(recipe_id)

        # Create a new Photo object
        photo = model.Photo(
            user_id=current_user.id,
            recipe_id=recipe.id,
            file_extension=file_extension
        )
        db.session.add(photo)
        db.session.commit()

        # Save the file
        path = (
            pathlib.Path(current_app.root_path)
            / "static"
            / "photos"
            / f"photo-{photo.id}.{file_extension}"
        )
        uploaded_file.save(path)

        return redirect(url_for('main.recipe', recipe_id=recipe.id))

    return abort(400, "No file uploaded")

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