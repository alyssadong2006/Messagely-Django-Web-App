"""tests for views"""
import pytest

# Needed for database
pytestmark = pytest.mark.django_db

def test_index_ok(client):
    """test if website runs properly"""
    response = client.get('/')
    assert response.status_code == 200
    