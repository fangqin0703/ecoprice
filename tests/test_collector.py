import pytest
from unittest.mock import patch
from src.collector import fetch_market_data

@patch('src.collector.requests.get')
def test_fetch_market_data_success(mock_get):
    """Test collector fetching data successfully."""
    # Mock the response object
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "products": [
            {"title": "Test Phone", "price": 299.99}
        ]
    }
    
    data = fetch_market_data()
    assert len(data) == 1
    assert data[0]['title'] == "Test Phone"
    assert data[0]['price'] == 299.99

@patch('src.collector.requests.get')
def test_fetch_market_data_failure(mock_get):
    """Test collector handling API failure."""
    mock_get.return_value.status_code = 500
    
    data = fetch_market_data()
    assert len(data) == 0
