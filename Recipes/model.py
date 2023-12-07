from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import flask_login
from sqlalchemy import DateTime
from sqlalchemy.sql import func


class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    recipes = db.relationship('Recipe', backref='author', lazy='dynamic')
    ratings = db.relationship('Rating', backref='rated_by', lazy='dynamic')
    photos = db.relationship('Photo', backref='uploaded_by', lazy='dynamic')
    profile_image = db.Column(db.String(100), nullable=False, default='photos/users/default.png')
    sign_up_date = db.Column(DateTime(timezone=True), server_default=func.now())
    bio = db.Column(db.String(256), nullable=True, default="Welcome to my kitchen in RecipeRealm! Here, I'll share my favorite recipes, and culinary adventures. Can't wait to connect with fellow food enthusiasts and exchange delicious ideas. Let's embark on this flavorful journey together!")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    servings = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)  # In minutes
    quantified_ingredients = db.relationship('QuantifiedIngredient', backref='recipe', lazy=True)
    steps = db.relationship('Step', backref='recipe', order_by="Step.sequence_number", lazy=True)
    ratings = db.relationship('Rating', backref='recipe', lazy=True)
    photos = db.relationship('Photo', backref='recipe', lazy=True)
    type_food = db.Column(db.String(200), nullable=False) # cuisine: asian, spanish...
    category_food = db.Column(db.String(200), nullable=False) # dessert, meal...

    def get_average(self):
        if self.ratings:
            total_score = sum(rating.value for rating in self.ratings)
            average = total_score / len(self.ratings)
            return round(average, 1)
        else:
            return None


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantified_ingredients = db.relationship('QuantifiedIngredient', backref='ingredient', lazy=True)


class QuantifiedIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    quantity = db.Column(db.String(100), nullable=False)
    unit_of_measurement = db.Column(db.String(50))


class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    sequence_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', backref='bookmarks')


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    file_extension = db.Column(db.String(10), nullable=False)
    