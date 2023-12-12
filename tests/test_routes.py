import pytest
from app import app, Recipe

@pytest.mark.usefixtures("test_client")
class TestApplicationRoutes:
    def test_main_page(self, test_client):
        response = test_client.get('/')
        assert response.status_code == 200

    def test_refresh_database(self, test_client, mocker):
        mocker.patch('app.get_recipes', return_value=[{'title': 'Mock Recipe', 'image': 'mock_image.jpg'}])
        response = test_client.post('/', data={"ingredients": "cheese", "refresh": "Refresh Database"})
        assert response.status_code == 200
        assert "Database refreshed" in response.data.decode()

    def test_database_entry_creation(self, test_client, mocker):
        with app.app_context():
            mocker.patch('app.get_recipes', return_value=[{'title': 'New Recipe', 'image': 'new_image.jpg'}])
            test_client.post('/', data={"ingredients": "cheese", "refresh": "Refresh Database"})
            recipe = Recipe.query.filter_by(title='New Recipe').first()
            assert recipe is not None
            assert recipe.image == 'new_image.jpg'

    def test_api_failure_handling(self, test_client, mocker):
        mocker.patch('app.get_recipes', side_effect=Exception("API failure"))
        response = test_client.post('/', data={"ingredients": "cheese", "refresh": "Refresh Database"})
        assert response.status_code == 200
        assert "Error: API failure" in response.data.decode()

    def test_empty_ingredient_search(self, test_client):
        response = test_client.post('/', data={"ingredients": "", "search": "Search Recipes"})
        assert response.status_code == 200
        assert "Ingredients: [List or Description of Ingredients Here]" in response.data.decode()

    def test_external_api_call_mocking(self, test_client, mocker):
        mock_data = [{'title': 'Mock Recipe', 'image': 'mock_image.jpg'}]
        mocker.patch('app.get_recipes', return_value=mock_data)
        response = test_client.post('/', data={"ingredients": "onion", "refresh": "Refresh Database"})
        assert response.status_code == 200
        assert "Database refreshed" in response.data.decode()