import datetime
import dateutil.tz
from flask import Blueprint, render_template
from . import model

bp = Blueprint("main", __name__)