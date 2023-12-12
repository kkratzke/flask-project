#!/usr/bin/env python3

import requests
from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe_app.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    image = db.Column(db.String(255))
    cuisine = db.Column(db.String(100))
    diet = db.Column(db.String(100))
    intolerances = db.Column(db.String(100))
    calories = db.Column(db.Integer)
    protein = db.Column(db.String(50))
    carbohydrates = db.Column(db.String(50))
    fat = db.Column(db.String(50))
    sugar = db.Column(db.String(50))
    sodium = db.Column(db.String(50))
    fiber = db.Column(db.String(50))


def init_db():
    with app.app_context():
        db.create_all()

def get_recipes(ingredients, cuisine="", diet="", intolerances=""):
    api_key = "f060e32f6f394b4b9ba6066a76bf9b61"
    ingredients_str = ",".join(ingredients)
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients_str}&addRecipeInformation=true&cuisine={cuisine}&diet={diet}&intolerances={intolerances}&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []


@app.route("/", methods=["GET", "POST"])
def main():
    recipe_html = ""
    sort_by = request.args.get('sort_by', 'title')
    sort_order = request.args.get('sort_order', 'asc')

    if request.method == "POST":
        if "search" in request.form:
            search_query = request.form.get("ingredients", "").strip()
            if search_query:
                query = Recipe.query.filter(Recipe.title.like(f"%{search_query}%"))
            else:
                query = Recipe.query

            if sort_by in ['calories', 'protein', 'fat', 'fiber']:
                if sort_order == 'desc':
                    query = query.order_by(db.desc(getattr(Recipe, sort_by)))
                else:
                    query = query.order_by(getattr(Recipe, sort_by))

            recipes = query.all()

            recipe_html = "<table><tr><th>Title</th><th>Calories</th><th>Protein</th><th>Carbohydrates</th><th>Fat</th><th>Fiber</th></tr>"
            for recipe in recipes:
                recipe_html += f"""
                    <tr>
                        <td>{recipe.title}</td>
                        <td>{recipe.calories}</td>
                        <td>{recipe.protein}</td>
                        <td>{recipe.carbohydrates}</td>
                        <td>{recipe.fat}</td>
                        <td>{recipe.fiber}</td>
                    </tr>
                """
            recipe_html += "</table>"

        elif "refresh" in request.form:
            ingredients = request.form.get("ingredients", "").split(',')
            try:
                recipes_data = get_recipes(ingredients)
                for recipe_data in recipes_data:
                    if not Recipe.query.filter_by(title=recipe_data.get('title')).first():
                        nutrition = recipe_data.get('nutrition', {})
                        nutrients = {nutrient['title']: nutrient['amount'] for nutrient in nutrition.get('nutrients', [])}
                        
                        recipe = Recipe(
                            title=recipe_data.get('title'),
                            image=recipe_data.get('image'),
                            cuisine="",
                            diet="",
                            intolerances="",
                            calories=nutrients.get('Calories'),
                            protein=nutrients.get('Protein'),
                            carbohydrates=nutrients.get('Carbohydrates'),
                            fat=nutrients.get('Fat'),
                            sugar=nutrients.get('Sugar'),
                            sodium=nutrients.get('Sodium'),
                            fiber=nutrients.get('Fiber')
                        )
                        db.session.add(recipe)
                db.session.commit()
                return "<p>Database refreshed!</p>"
            except Exception as e:
                return f"<p>Error: {e}</p>"

    else:
        query = Recipe.query
        if sort_by in ['calories', 'protein', 'fat', 'fiber']:
            if sort_order == 'desc':
                query = query.order_by(db.desc(getattr(Recipe, sort_by)))
            else:
                query = query.order_by(getattr(Recipe, sort_by))

        recipes = query.all()

    recipe_html = ""
    for recipe in recipes:
        recipe_html += f"<div><h3>{recipe.title}</h3><p>Calories: {recipe.calories}</p><p>Protein: {recipe.protein}</p><p>Carbohydrates: {recipe.carbohydrates}</p><p>Fat: {recipe.fat}</p><p>Fiber: {recipe.fiber}</p><p>Ingredients: [List or Description of Ingredients Here]</p></div>"


    return render_template_string('''
        <form action="/" method="POST">
            <input name="ingredients" placeholder="Enter ingredients separated by commas">
            <select name="sort_by">
                <option value="title">Title</option>
                <option value="calories">Calories</option>
                <option value="protein">Protein</option>
                <option value="fat">Fat</option>
                <option value="fiber">Fiber</option>
            </select>
            <select name="sort_order">
                <option value="asc">Ascending</option>
                <option value="desc">Descending</option>
            </select>
            <input type="submit" name="search" value="Search Recipes">
            <input type="submit" name="refresh" value="Refresh from API">
        </form>
        <div>{{ recipe_list|safe }}</div>
        ''', recipe_list=recipe_html)

if __name__ == '__main__':
    app.run(debug=True)
