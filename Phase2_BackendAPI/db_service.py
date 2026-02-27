import sqlite3
import os

def get_db_path():
    # Allow tests to override the DB path
    return os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), '..', 'Phase1_DataPipeline', 'zomato.db'))

def get_candidates(place: str, cuisine: str, max_price: float = None, min_rating: float = None, limit: int = 20):
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = """
    SELECT name, address, MAX(rate_num) as rate, MIN(cost_num) as cost, MAX(cuisines) as cuisines, MAX(url) as url
    FROM restaurants 
    WHERE location LIKE ? AND cuisines LIKE ?
    GROUP BY name
    """
    
    params = [f"%{place}%", f"%{cuisine}%"]
    
    if max_price is not None:
        query += " AND cost_num <= ?"
        params.append(max_price)
        
    if min_rating is not None:
        query += " AND rate_num >= ?"
        params.append(min_rating)
        
    query += " ORDER BY rate_num DESC, votes DESC LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    candidates = [dict(row) for row in rows]
    conn.close()
    
    return candidates

def get_options(location: str = None):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    
    # Locations
    cursor.execute("SELECT DISTINCT location FROM restaurants WHERE location IS NOT NULL AND location != 'Unknown' ORDER BY location")
    locations = [row[0] for row in cursor.fetchall() if row[0]]
    
    # Cuisines
    if location:
        cursor.execute("SELECT DISTINCT cuisines FROM restaurants WHERE cuisines IS NOT NULL AND cuisines != 'Unknown' AND location = ?", (location,))
    else:
        cursor.execute("SELECT DISTINCT cuisines FROM restaurants WHERE cuisines IS NOT NULL AND cuisines != 'Unknown'")
        
    cuisine_rows = cursor.fetchall()
    cuisines_set = set()
    for row in cuisine_rows:
        if row[0]:
            for c in row[0].split(','):
                cuisines_set.add(c.strip())
    
    cuisines = sorted(list(cuisines_set))
    conn.close()
    
    return {
        "locations": locations,
        "cuisines": cuisines
    }
