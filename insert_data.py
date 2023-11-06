from Recipes import create_app, db
from Recipes.model import User, Recipe, Ingredient, QuantifiedIngredient, Step, Rating, Photo

app = create_app()
with app.app_context():
    # Crear todas las tablas
    db.create_all()

    # Usuarios
    user1 = User(name='Chef A', email='chefa@example.com')
    user1.set_password('password123')
    user2 = User(name='Chef B', email='chefb@example.com')
    user2.set_password('password123')

    db.session.add(user1)
    db.session.add(user2)
    
    # Ingredientes
    ingredient1 = Ingredient(name='Harina')
    ingredient2 = Ingredient(name='Azúcar')

    db.session.add(ingredient1)
    db.session.add(ingredient2)
    
    # Recetas
    recipe1 = Recipe(title='Pastel de Chocolate', description='Un delicioso pastel de chocolate.', author=user1)
    
    db.session.add(recipe1)
    
    # Ingredientes cuantificados para la receta
    q_ingredient1 = QuantifiedIngredient(quantity='200g', unit_of_measurement='gramos', ingredient=ingredient1, recipe=recipe1)
    q_ingredient2 = QuantifiedIngredient(quantity='100g', unit_of_measurement='gramos', ingredient=ingredient2, recipe=recipe1)

    db.session.add(q_ingredient1)
    db.session.add(q_ingredient2)
    
    # Pasos para la receta
    step1 = Step(sequence_number=1, description='Mezclar la harina y el azúcar.', recipe=recipe1)
    step2 = Step(sequence_number=2, description='Hornear a 180 grados durante 30 minutos.', recipe=recipe1)

    db.session.add(step1)
    db.session.add(step2)
    
    # Ratings
    rating1 = Rating(value=5, recipe=recipe1, rated_by=user2)
    
    db.session.add(rating1)
    
    # Fotos
    # photo1 = Photo(file_extension='.jpg', recipe=recipe1, uploaded_by=user1)

    # db.session.add(photo1)

    # Guardar todo en la base de datos
    db.session.commit()

    print('Datos de ejemplo insertados en la base de datos.')
