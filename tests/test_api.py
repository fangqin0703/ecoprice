import pytest
from src.api import app, db
from src.models import DeviceData

@pytest.fixture
def client():
    # Configure the app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            # Insert some dummy data
            dev1 = DeviceData(title="iPhone 13 Refurbished", price=450.0, eco_score=77.5)
            dev2 = DeviceData(title="Samsung S22 Ultra", price=600.0, eco_score=70.0)
            db.session.add(dev1)
            db.session.add(dev2)
            db.session.commit()
            
        yield client

def test_api_get_devices(client):
    """Test the API endpoint returns devices correctly."""
    response = client.get('/api/devices')
    assert response.status_code == 200
    
    data = response.get_json()
    assert len(data) == 2
    
    titles = [d['title'] for d in data]
    assert "iPhone 13 Refurbished" in titles
    assert "Samsung S22 Ultra" in titles
    
    for d in data:
        assert 'id' in d
        assert 'price' in d
        assert 'eco_score' in d
        assert 'date_fetched' in d
