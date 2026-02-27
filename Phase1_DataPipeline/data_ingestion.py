import os
import sqlite3
import pandas as pd
from datasets import load_dataset, disable_progress_bar

def clean_rate(rate_str):
    if pd.isna(rate_str):
        return None
    rate_str = str(rate_str).strip()
    if rate_str in ['NEW', '-'] or rate_str == '':
        return None
    # '4.1/5' -> 4.1
    try:
        return float(rate_str.split('/')[0].strip())
    except:
        return None

def clean_cost(cost_str):
    if pd.isna(cost_str):
        return None
    cost_str = str(cost_str).strip().replace(',', '')
    try:
        return float(cost_str)
    except:
        return None

def ingest_data(db_path='zomato.db', limit=None):
    disable_progress_bar()
    print("Loading dataset from Hugging Face...")
    dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation")
    df = dataset['train'].to_pandas()
    
    if limit:
        df = df.head(limit)

    print(f"Loaded {len(df)} rows. Cleaning data...")
    
    # Rename complex columns for easier SQL usage
    df = df.rename(columns={
        'approx_cost(for two people)': 'approx_cost',
        'listed_in(type)': 'listed_type',
        'listed_in(city)': 'listed_city'
    })
    
    # Clean rate
    df['rate_num'] = df['rate'].apply(clean_rate)
    
    # Clean cost
    df['cost_num'] = df['approx_cost'].apply(clean_cost)
    
    # Fill NAs
    df['cuisines'] = df['cuisines'].fillna('Unknown')
    df['location'] = df['location'].fillna('Unknown')
    df['name'] = df['name'].fillna('Unknown')
    
    print(f"Saving to SQLite at {db_path}...")
    conn = sqlite3.connect(db_path)
    df.to_sql('restaurants', conn, if_exists='replace', index=False)
    
    # Create indexes for quick retrieval
    conn.execute("CREATE INDEX IF NOT EXISTS idx_location ON restaurants(location)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_cuisines ON restaurants(cuisines)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_rate ON restaurants(rate_num)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_cost ON restaurants(cost_num)")
    
    conn.close()
    print("Data ingestion complete.")
    return df

if __name__ == "__main__":
    ingest_data()
