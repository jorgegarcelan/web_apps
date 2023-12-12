from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileAllowed, FileRequired
from .model import Ingredient

def ingredient_choices():
    return Ingredient.query.all()


class IngredientForm(FlaskForm):
    new_ingredient = StringField('Ingredient', validators=[Length(max=100)])
    quantity = StringField('Quantity', validators=[DataRequired(), Length(max=100)])
    unit_of_measurement = StringField('Unit of Measurement', validators=[Length(max=50)])
    submit = SubmitField('Add Ingredients')


class StepForm(FlaskForm):
    sequence_number = IntegerField('Step Number', validators=[DataRequired(), NumberRange(min=1)])
    step_description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Steps')


class RecipeForm(FlaskForm):
    """Formulario principal para crear una receta."""
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    servings = IntegerField('Number of Servings', validators=[DataRequired(), NumberRange(min=1, max=10)])
    cook_time = IntegerField('Cook Time (in minutes)', validators=[DataRequired(), NumberRange(min=1)])
    image = FileField('Recipe Image', validators=[
        FileRequired(), 
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    type_food = SelectField(
        'Type of Cuisine', 
        choices=[('Mexican', 'Mexican'), ("Japanese", "Japanese"), ("Chinese", "Chinese"), ("Korean", "Korean"),
                 ("Thai", "Thai"), ("Indian", "Indian"), ("American", "American"), ("Spanish", "Spanish"), ("Italian", "Italian"),
                 ("French", "French"), ("Eastern Europe", "Eastern Europe"), ("Arab", "Arab"), ("African", "African"), ("Other", "Other")],
        validators=[DataRequired()]
    )
    category_food = SelectField(
        'Category of Food', 
        choices=[("Breakfast", "Breakfast"), ("Meal", "Meal"), ("Brunch", "Brunch"), ("Snack", "Snack"), ("Dessert", "Dessert"), ("Other", "Other")],
        validators=[DataRequired()]
    )
    submit = SubmitField('Create Recipe')