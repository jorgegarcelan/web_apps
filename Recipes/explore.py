from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db


bp = Blueprint("explore", __name__)

@bp.route("/explore")
def search():
    return render_template('recipes/explore.html')