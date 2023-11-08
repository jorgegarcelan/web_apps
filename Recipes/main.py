import datetime
import dateutil.tz
from flask import Blueprint, render_template, abort
import flask_login
from . import model
from Recipes import db, create_app

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("main/main.html")

@bp.route("/user/<int:user_id>")
@flask_login.login_required
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