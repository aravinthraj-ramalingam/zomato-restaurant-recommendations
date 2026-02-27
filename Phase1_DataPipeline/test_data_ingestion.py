import os
import sqlite3
import pytest
from data_ingestion import ingest_data, clean_rate, clean_cost

TEST_DB_PATH = 'test_zomato.db'

def setup_module(module):
    # Run ingestion with a small limit for testing
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    ingest_data(db_path=TEST_DB_PATH, limit=100)

def teardown_module(module):
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_clean_rate():
    assert clean_rate('4.1/5') == 4.1
    assert clean_rate('NEW') is None
    assert clean_rate('-') is None
    assert clean_rate(None) is None

def test_clean_cost():
    assert clean_cost('1,200') == 1200.0
    assert clean_cost('800') == 800.0
    assert clean_cost(None) is None
    assert clean_cost('abc') is None

def test_db_creation():
    assert os.path.exists(TEST_DB_PATH)
    
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='restaurants'")
    assert cursor.fetchone() is not None
    
    # Check row count
    cursor.execute("SELECT COUNT(*) FROM restaurants")
    count = cursor.fetchone()[0]
    assert count == 100
    
    # Check if cleaned columns exist
    cursor.execute("PRAGMA table_info(restaurants)")
    columns = [row[1] for row in cursor.fetchall()]
    assert 'rate_num' in columns
    assert 'cost_num' in columns
    assert 'approx_cost' in columns
    
    conn.close()
