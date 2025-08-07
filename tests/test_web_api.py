import pytest
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Test the main route returns HTML"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Simple Spreadsheet' in response.data


def test_evaluate_api(client):
    """Test the evaluate API endpoint"""
    test_data = {
        'matrix': [
            ['42', '=A1+5'],
            ['3.14', '=B1']
        ]
    }
    
    response = client.post('/api/evaluate',
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['result'] == [[42.0, 47.0], [3.14, 47.0]]


def test_parse_cell_api(client):
    """Test the parse_cell API endpoint"""
    test_data = {'cell': '=A1+5'}
    
    response = client.post('/api/parse_cell',
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['ref1'] == 'A1'
    assert data['operator'] == '+'
    assert data['ref2'] == 5.0


def test_cell_to_index_api(client):
    """Test the cell_to_index API endpoint"""
    test_data = {'cell_ref': 'B2'}
    
    response = client.post('/api/cell_to_index',
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['row'] == 1
    assert data['col'] == 1


def test_read_cell_api(client):
    """Test the read_cell API endpoint"""
    test_data = {
        'cell': '=A1+5',
        'matrix': [['42']]
    }
    
    response = client.post('/api/read_cell',
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['result'] == 47.0


def test_error_handling(client):
    """Test API error handling"""
    # Test with invalid matrix
    test_data = {'matrix': []}
    
    response = client.post('/api/evaluate',
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] == False
    assert 'error' in data


def test_invalid_cell_reference(client):
    """Test error handling for invalid cell references"""
    test_data = {'cell_ref': 'invalid'}
    
    response = client.post('/api/cell_to_index',
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] == False
    assert 'error' in data
