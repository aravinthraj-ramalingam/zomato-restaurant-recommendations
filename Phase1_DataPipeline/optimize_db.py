import sqlite3
import os

def optimize():
    src_db = 'Phase1_DataPipeline/zomato.db'
    dest_dir = 'api'
    dest_db = os.path.join(dest_dir, 'zomato.db')
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    print(f"Optimizing {src_db} -> {dest_db}...")
    
    conn_src = sqlite3.connect(src_db)
    conn_dest = sqlite3.connect(dest_db)
    
    # Create the table with only necessary columns
    conn_dest.execute("""
    CREATE TABLE IF NOT EXISTS restaurants (
        name TEXT,
        address TEXT,
        rate_num REAL,
        cost_num REAL,
        cuisines TEXT,
        url TEXT,
        location TEXT,
        votes INTEGER
    )
    """)
    
    # Transfer data
    cursor = conn_src.cursor()
    cursor.execute("SELECT name, address, rate_num, cost_num, cuisines, url, location, votes FROM restaurants")
    
    rows = cursor.fetchall()
    conn_dest.executemany("INSERT INTO restaurants VALUES (?,?,?,?,?,?,?,?)", rows)
    
    # Create indexes for performance
    conn_dest.execute("CREATE INDEX IF NOT EXISTS idx_loc_cuis ON restaurants(location, cuisines)")
    conn_dest.execute("CREATE INDEX IF NOT EXISTS idx_name ON restaurants(name)")
    
    conn_dest.commit()
    
    # Clean up and vacuum to minimize size
    conn_dest.execute("VACUUM")
    
    conn_src.close()
    conn_dest.close()
    
    src_size = os.path.getsize(src_db) / (1024*1024)
    dest_size = os.path.getsize(dest_db) / (1024*1024)
    
    print(f"Done!")
    print(f"Source size: {src_size:.2f} MB")
    print(f"Optimized size: {dest_size:.2f} MB")

if __name__ == "__main__":
    optimize()
