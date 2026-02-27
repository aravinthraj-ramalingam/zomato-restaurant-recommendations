import os
import sqlite3
import pytest
from fastapi.testclient import TestClient
from main import app
from db_service import get_candidates

# Path logic for testing
TEST_DB_PATH = os.path.join(os.path.dirname(__file__), 'test_zomato.db')
os.environ["DB_PATH"] = TEST_DB_PATH

client = TestClient(app)

def setup_module(module):
    # Ensure test DB has some mock data
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS restaurants (name TEXT, address TEXT, rate_num REAL, cost_num REAL, cuisines TEXT, url TEXT, location TEXT, votes INTEGER)")
    cursor.execute("DELETE FROM restaurants")
    
    # Insert Mock Restaurant
    cursor.execute("INSERT INTO restaurants VALUES ('Spice Symphony', '123 Test St', 4.5, 800.0, 'North Indian, Chinese', 'http://test.com', 'TestCity', 500)")
    conn.commit()
    conn.close()

def teardown_module(module):
    if os.path.exists(TEST_DB_PATH):
        try:
            os.remove(TEST_DB_PATH)
        except Exception:
            pass

def test_get_candidates():
    candidates = get_candidates(place='TestCity', cuisine='North Indian', max_price=1000.0, min_rating=4.0)
    assert len(candidates) > 0
    assert candidates[0]['name'] == 'Spice Symphony'
    assert candidates[0]['cost'] == 800.0

def test_api_recommendation():
    response = client.post("/api/recommend", json={
        "place": "TestCity",
        "cuisine": "Chinese",
        "max_price": 1000,
        "min_rating": 4.0
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert "recommendations" in data
    assert "llm_rationale" in data
    assert len(data["recommendations"]) > 0
    assert data["recommendations"][0]["name"] == "Spice Symphony"
    
    # Verifying fallback text since we didn't mock GEMINI_API_KEY
    assert "missing" in data["llm_rationale"].lower() or "not find" in data["llm_rationale"].lower() or "offline" in data["llm_rationale"].lower()
