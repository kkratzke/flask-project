import pytest
from unittest.mock import patch
from app import get_recipes

@patch('app.requests.get')
def test_get_recipes(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = [{'title': 'Mock Recipe', 'id': 123}]

    response = get_recipes(['ingredient1', 'ingredient2'])

    mock_get.assert_called_once()
    assert len(response) == 1
    assert response[0]['title'] == 'Mock Recipe'
    assert response[0]['id'] == 123