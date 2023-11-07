import datetime
import dateutil.tz
from flask import Blueprint, render_template
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
    query_u = db.select(model.User).where(model.User.id == user_id)
    user = db.session.execute(query_u).scalar_one_or_none()
    print(user)
    
    """
    query_p = db.select(model.Message).where(model.Message.user_id == user_id).where(model.Message.response_to_id == None).order_by(model.Message.timestamp.desc()) # get messages that are not responses
    posts = db.session.execute(query_p).scalars().all()
    #print(posts)

    if not posts:
        abort(404, "Posts for User id {} doesn't exist.".format(user_id))

    return render_template("main/user.html", posts=posts, user=user)
    """
    
    return render_template("user/user.html", user=user)