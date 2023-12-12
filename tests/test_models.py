import pytest
from app import Recipe, db

def test_recipe_creation():
    recipe = Recipe(
        title='Test Recipe',
        image='test_image.jpg',
        cuisine='Italian',
        diet='Vegetarian',
        intolerances='Nuts',
        calories=350,
        protein='25g',
        carbohydrates='30g',
        fat='20g',
        sugar='5g',
        sodium='200mg',
        fiber='10g'
    )

    assert recipe.title == 'Test Recipe'
    assert recipe.image == 'test_image.jpg'
    assert recipe.cuisine == 'Italian'
    assert recipe.diet == 'Vegetarian'
    assert recipe.intolerances == 'Nuts'
    assert recipe.calories == 350
    assert recipe.protein == '25g'
    assert recipe.carbohydrates == '30g'
    assert recipe.fat == '20g'
    assert recipe.sugar == '5g'
    assert recipe.sodium == '200mg'
    assert recipe.fiber == '10g'
