import datetime
import dateutil.tz
from flask import Blueprint, render_template, abort
import flask_login
from . import model, gpt
from Recipes import db, create_app
from gpt import gpt4_vision

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("main/main.html")

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

    
    return render_template("recipes/recipes.html", recipe=recipe)

@bp.route("/recipe_vision")
def recipe_vision():

    image = request.form
    output = gpt4_vision(image)

    return render_template("gpt/gpt4vision.html", )