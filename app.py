from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import request, render_template, redirect, url_for

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://stas:stas@localhost/testpost'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем уведомления об изменениях в базе данных

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Recepies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    category = db.Column(db.String(50))
    description = db.Column(db.String(10))
    cooktime = db.Column(db.String)
    ingredients = db.Column(db.String)

@app.route('/addrecipe', methods = ['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        description = request.form.get('description')
        cooktime = request.form.get('cooktime')
        ingredients = request.form.get('ingredients')

        if not name or not category or not description or not cooktime or not ingredients:
            return "Заполните все поля!", 400

        new_recipe = Recepies(
            name=name,
            category=category,
            description=description,
            cooktime=cooktime,
            ingredients=ingredients,
        )
        db.session.add(new_recipe)
        db.session.commit()

        return redirect(url_for('list_recipes'))

    return render_template('add_recipe.html')

@app.route('/recipes', methods=['GET'])
def list_recipes():
    recipes = Recepies.query.all()
    return render_template('list_recipes.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)