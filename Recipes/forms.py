from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class IngredientForm(FlaskForm):
    """Subformulario para ingredientes."""
    name = StringField('Ingredient Name', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])

class StepForm(FlaskForm):
    """Subformulario para pasos de la receta."""
    description = TextAreaField('Step Description', validators=[DataRequired()])

class RecipeForm(FlaskForm):
    """Formulario principal para crear una receta."""
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    servings = IntegerField('Number of Servings', validators=[DataRequired(), NumberRange(min=1)])
    cook_time = IntegerField('Cook Time (in minutes)', validators=[DataRequired(), NumberRange(min=1)])
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    steps = FieldList(FormField(StepForm), min_entries=1)
    submit = SubmitField('Create Recipe')