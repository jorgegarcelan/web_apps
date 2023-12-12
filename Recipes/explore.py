from flask import Blueprint, render_template, request
from . import db
from .model import Recipe, Rating
from sqlalchemy import func


bp = Blueprint("explore", __name__)


@bp.route("/explore")
def search():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    per_page = 5

    type_food = request.args.get('type_food')
    category_food = request.args.get('category_food')
    servings = request.args.get('servings')
    cook_time = request.args.get('cook_time')

    recipes_query = Recipe.query

    if search_query:
        recipes_query = recipes_query.filter(Recipe.title.like(f'%{search_query}%'))
    if type_food:
        recipes_query = recipes_query.filter(Recipe.type_food == type_food)
    if category_food:
        recipes_query = recipes_query.filter(Recipe.category_food == category_food)
    if servings:
        recipes_query = recipes_query.filter(Recipe.servings == int(servings))
    if cook_time:
        if '-' in cook_time:
            min_time, max_time = cook_time.split('-')
            recipes_query = recipes_query.filter(Recipe.cook_time.between(int(min_time), int(max_time)))
        elif cook_time == '120+':
            recipes_query = recipes_query.filter(Recipe.cook_time >= 120)

    # Order the results by rating.
    subq = db.session.query(
        Rating.recipe_id,
        func.avg(Rating.value).label('average_rating')
    ).group_by(Rating.recipe_id).subquery()
    recipes_query = recipes_query.outerjoin(subq, Recipe.id == subq.c.recipe_id).order_by(subq.c.average_rating.desc(), Recipe.id)

    paginated_recipes = recipes_query.paginate(page=page, per_page=per_page)
    filter_params = {
        'search_query': search_query,
        'type_food': type_food,
        'category_food': category_food,
        'servings': servings,
        'cook_time': cook_time,
    }

    return render_template('recipes/explore.html', 
                           paginated_recipes=paginated_recipes, 
                           **filter_params)