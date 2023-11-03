import datetime
import dateutil.tz
from flask import Blueprint, render_template
from . import model

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("main/main.html")