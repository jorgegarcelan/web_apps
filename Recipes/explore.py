from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .model import Recipe


bp = Blueprint("explore", __name__)

@bp.route("/explore")
def search():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    per_page = 5

    if search_query:
        recipes_query = Recipe.query.filter(Recipe.title.like(f'%{search_query}%'))
    else:
        recipes_query = Recipe.query

    paginated_recipes = recipes_query.paginate(page=page, per_page=per_page)

    return render_template('recipes/explore.html', 
                           paginated_recipes=paginated_recipes, 
                           search_query=search_query)