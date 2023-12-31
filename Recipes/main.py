from flask import Blueprint, render_template, abort, request, url_for, flash, redirect, current_app
from flask_login import current_user, login_required
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename
from Recipes import db, gpt
from .forms import RecipeForm, IngredientForm, StepForm
from .model import Recipe, Ingredient, QuantifiedIngredient, Step, Photo
from . import model
import os
import numpy as np
import pathlib


bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    """
    Home page route showing top recipes based on average rating.
    """
    top_recipes = db.session.query(
        model.Recipe, 
        func.avg(model.Rating.value).label('average_rating')
    ).join(model.Rating).group_by(model.Recipe.id).order_by(func.avg(model.Rating.value).desc()).limit(5).all()

    return render_template('main/main.html', top_recipes=top_recipes)


@bp.route("/user/<int:user_id>")
def user(user_id):
    """
    User profile route showing user details, recipes, bookmarks, and photos.
    """
    # Fetch user details
    query_u = db.select(model.User).where(model.User.id == user_id)
    user = db.session.execute(query_u).scalar_one_or_none()
    
    # Fetch user recipes with average ratings
    recipes = db.session.query(
        model.Recipe,
        func.coalesce(func.round(func.avg(model.Rating.value), 1), 0).label('average_rating')
    ).outerjoin(model.Rating, model.Rating.recipe_id == model.Recipe.id) \
    .filter(model.Recipe.user_id == user_id) \
    .group_by(model.Recipe.id, model.Recipe.title) \
    .all()

    # Fetch bookmarked recipes
    bookmarked_recipes = db.session.query(
        model.Recipe,
        func.round(func.avg(model.Rating.value), 1).label('average_rating')
    ).join(model.Bookmark, model.Bookmark.recipe_id == model.Recipe.id) \
    .join(model.Rating, model.Rating.recipe_id == model.Recipe.id, isouter=True) \
    .filter(model.Bookmark.user_id == user_id) \
    .group_by(model.Recipe.id) \
    .all()

    # Fetch user photos
    query_p = db.select(model.Photo).where(model.Photo.user_id == user_id)
    photos = db.session.execute(query_p).scalars().all()
    
    return render_template("user/user.html", user=user, recipes=recipes, bookmarked_recipes=bookmarked_recipes, photos=photos)


@bp.route("/recipes/<int:recipe_id>")
def recipe(recipe_id):
    """
    Display a recipe page with detailed information, including ingredients, user ratings, and photos.
    """
    # Fetch recipe details
    query_r = db.select(model.Recipe).where(model.Recipe.id == recipe_id)
    recipe = db.session.execute(query_r).scalar_one_or_none()
    
    # Fetch user details
    query_u = db.select(model.User).where(model.User.id == recipe.user_id)
    user = db.session.execute(query_u).scalar_one_or_none()
    
    # Fetch ingredients information
    quantified_ingredients = model.QuantifiedIngredient.query.filter_by(recipe_id=recipe_id).all()     # Query the QuantifiedIngredient model to get all entries related to the recipe_id
    ingredients_info = [{'name': qi.ingredient.name, 'quantity': qi.quantity, 'unit_of_measurement': qi.unit_of_measurement} for qi in quantified_ingredients]

    if current_user.is_authenticated:
        bookmark = model.Bookmark.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
        is_bookmarked = bookmark is not None
        your_photos = model.Photo.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).all()
        rate = model.Rating.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()      # Query to check if the current user has rated the recipe
        is_rated = rate is not None
    else:
        is_bookmarked, your_photos, is_rated = None, None, None

    # Fetch recipe photos and ratings
    chef_photos = model.Photo.query.filter_by(user_id=user.id, recipe_id=recipe_id).all()
    query_rt = db.select(model.Rating.value).where(model.Rating.recipe_id == recipe_id)
    ratings_list = db.session.execute(query_rt).scalars().all()
    
    # Compute average rating
    count = len(ratings_list)
    if count == 0:
        rating, count, current_rate = "No reviews yet", "", ""
        return render_template("recipes/recipes.html", recipe=recipe, user=user, rating=rating, current_rate=current_rate, count=count, ingredients_info=ingredients_info, is_bookmarked=is_bookmarked, is_rated=is_rated, chef_photos=chef_photos, your_photos=your_photos)
        
    else:
        count = f"({count})"
        rating = round(np.mean(ratings_list), 1)
        rating = str(rating) + " / 5"
        if not is_rated:
            current_rate = ""
        else:
            current_rate = rate.value
        
        return render_template("recipes/recipes.html", recipe=recipe, user=user, rating=rating, current_rate=current_rate, count=count, ingredients_info=ingredients_info, is_bookmarked=is_bookmarked, is_rated=is_rated, chef_photos=chef_photos, your_photos=your_photos)


@bp.route('/edit_user', methods=['POST'])
def edit_user():
    """
    Handle the POST request to edit a user's profile information.
    """
    user_id = request.form.get('user_id')
    name = request.form.get('edit_name')
    bio = request.form.get('edit_bio')
    email = request.form.get('edit_email')
    uploaded_file = request.files['profile_image_input']

    # Fetch and update user data
    user = model.User.query.get_or_404(user_id)
    user.name, user.bio, user.email = name, bio, email

    # Handle profile image upload
    if uploaded_file.filename:
        content_type = uploaded_file.content_type
        if content_type == "image/png":
            file_extension = "png"
        elif content_type == "image/jpeg":
            file_extension = "jpg"
        else:
            abort(400, f"Unsupported file type {content_type}")

        # Save the file
        path = (
            pathlib.Path(current_app.root_path)
            / "static"
            / "photos" 
            / "users"
            / f"user-{user.id}.{file_extension}"
        )
        uploaded_file.save(path)

        user.profile_image = f"user-{user.id}.{file_extension}"

    # Commit the changes to the database
    db.session.commit()
    return redirect(url_for('main.user', user_id=user_id))


@bp.route('/edit_recipe', methods=['POST'])
def edit_recipe():
    """
    Handle POST request to edit a recipe's details.
    """
    # Get data from the submitted form
    recipe_id = request.form.get('recipe_id')
    name = request.form.get('edit_name')
    description = request.form.get('edit_description')
    servings = request.form.get('edit_servings')
    cook_time = request.form.get('edit_cook_time')
    type_food = request.form.get('edit_type_food')
    category_food = request.form.get('edit_category_food')

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
    return redirect(url_for('main.recipe', recipe_id=recipe_id))


@bp.route('/bookmark', methods=['POST'])
def bookmark_recipe():
    """
    Toggle bookmark status for a recipe.
    """
    # Get data from the submitted form
    recipe_id = request.form.get('recipe_id')

    # Check if bookmark already exists
    bookmark = model.Bookmark.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
    
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
    else:
        new_bookmark = model.Bookmark(user_id=current_user.id, recipe_id=recipe_id)
        db.session.add(new_bookmark)
        db.session.commit()

    return redirect(url_for('main.recipe', recipe_id=recipe_id))


@bp.route('/rate_recipe', methods=['POST'])
@login_required
def rate_recipe():
    """
    Rate a recipe by the current user.
    """
    # Get data from the submitted form
    rating_value = request.form.get('rating')
    recipe_id = request.form.get('recipe_id')

    # Check if the rating already exists for the user and recipe
    rating = model.Rating.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()

    if rating:
        rating.value = rating_value
    else:
        new_rating = model.Rating(user_id=current_user.id, recipe_id=recipe_id, value=rating_value)
        db.session.add(new_rating)

    db.session.commit()
    return redirect(url_for('main.recipe', recipe_id=recipe_id))


@bp.route('/upload_photo', methods=['POST'])
def upload_photo():
    """
    Handle photo upload for a recipe.
    """
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
            / "recipes"
            / f"photo-{photo.id}.{file_extension}"
        )
        uploaded_file.save(path)

        return redirect(url_for('main.recipe', recipe_id=recipe.id))

    return abort(400, "No file uploaded")


@bp.route('/delete_photo', methods=['POST', 'DELETE'])
def delete_photo():
    """
    Delete a specific photo associated with a recipe or user.
    """
    # Get data from form
    photo_id = request.form.get('photo_id')
    recipe_id = request.form.get('recipe_id')
    user_id = request.form.get('user_id')

    # Find the photo by ID
    photo = Photo.query.get(photo_id)

    # Fetch recipe photos
    photos = model.Photo.query.all()

    # do not delete if photo is the first photo of the recipe (it is the principal for that recipe)
    if photo_id == str(photos[0].id):
        abort(400, "Error while deleting the photo: You can not remove the default photo for that recipe")
    
    else:
        # Find the photo by ID
        photo = Photo.query.get(photo_id)
        if photo:
            # Delete the file from the file system
            path = ( pathlib.Path(current_app.root_path)
                / "static"
                / "photos"
                / "recipes"
                / f"photo-{photo.id}.{photo.file_extension}" )
            
            os.remove(path)
            # Delete the record from the database
            db.session.delete(photo)
            db.session.commit()

            if recipe_id != None:
                return redirect(url_for('main.recipe', recipe_id=recipe_id))
            if user_id != None:
                return redirect(url_for('main.user', user_id=user_id))
        
        return abort(400, "Error while deleting the photo")


@bp.route("/recipe_vision", methods=['GET', 'POST'])
def recipe_vision():
    """
    Handle recipe suggestions based on image input using GPT model.
    """
    if request.method == 'POST':
        file = request.files.get('file')

        if not file or file.filename == '':
            return 'No selected file'

        # Save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join('Recipes/static/imgs', filename)
        file.save(filepath)

        # Process the image with your GPT model here
        try:
            output = gpt.gpt4_vision(filepath)
        except:
            return abort(400, "There was a problem with the image")

        # URL for the uploaded image
        uploaded_image_url = url_for('static', filename='imgs/' + filename)
        return render_template("gpt/gpt4vision.html", output=output, uploaded_image=uploaded_image_url)

    return render_template("gpt/gpt4vision.html")


@bp.route('/create_recipe', methods=['GET', 'POST'])
@login_required
def create_recipe():
    """
    Route to create a new recipe, handling both display and form submission.
    """
    recipe_form = RecipeForm()
    ingredient_form = IngredientForm()
    step_form = StepForm()

    if request.method == 'POST':
        ingredientes_agregados = False
        pasos_agregados = False

        if recipe_form.validate_on_submit():
            new_recipe = Recipe(
                title=recipe_form.title.data,
                description=recipe_form.description.data,
                servings=recipe_form.servings.data,
                cook_time=recipe_form.cook_time.data,
                category_food = recipe_form.category_food.data,
                type_food = recipe_form.type_food.data,
                user_id=current_user.id
            )
            db.session.add(new_recipe)
            db.session.flush()

            # Handle recipe image
            if recipe_form.image.data:
                image_file = recipe_form.image.data
                filename = secure_filename(image_file.filename)
                file_extension = os.path.splitext(filename)[1]
                file_extension = file_extension[1:]
                photo = Photo(
                    user_id=current_user.id,
                    recipe_id=new_recipe.id,
                    file_extension=file_extension
                )
                db.session.add(photo)
                db.session.flush()
                image_file.save(os.path.join('Recipes/static/photos/recipes', f"photo-{photo.id}.{file_extension}"))

            # Handle steps
            if 'step_description' in request.form:
                step_descriptions = request.form.getlist('step_description')
                for i, description in enumerate(step_descriptions):
                    if description.strip(): 
                        new_step = Step(
                            recipe_id=new_recipe.id,
                            sequence_number=i + 1,
                            description=description
                        )
                        db.session.add(new_step)
                pasos_agregados = True

            # Handle ingredients
            if 'new_ingredient' in request.form:
                ingredient_names = request.form.getlist('new_ingredient')
                ingredient_quantities = request.form.getlist('quantity')
                ingredient_units = request.form.getlist('unit_of_measurement')
                for name, quantity, unit in zip(ingredient_names, ingredient_quantities, ingredient_units):
                    if name: 
                        ingredient = Ingredient.query.filter_by(name=name).first()
                        if not ingredient:
                            ingredient = Ingredient(name=name)
                            db.session.add(ingredient)
                            db.session.flush()
                        quantified_ingredient = QuantifiedIngredient(
                            ingredient_id=ingredient.id,
                            recipe_id=new_recipe.id,
                            quantity=quantity,
                            unit_of_measurement = unit
                        )
                        db.session.add(quantified_ingredient)
                if ingredient_names:
                    ingredientes_agregados = True

            # Handle possible errors. Otherwise, finish the process.
            if ingredientes_agregados and pasos_agregados:
                db.session.commit()
                return redirect(url_for('explore.search'))
            else:
                db.session.rollback()
                if not ingredientes_agregados:
                    flash('Por favor, añade al menos un ingrediente.', 'create_error')
                if not pasos_agregados:
                    flash('Por favor, añade al menos un paso.', 'create_error')
        else:
            flash('Error en el formulario de recetas.', 'create_error')
        
    return render_template('create.html', recipe_form=recipe_form, ingredient_form=ingredient_form, step_form=step_form)