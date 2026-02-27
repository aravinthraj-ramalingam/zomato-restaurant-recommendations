import sqlite3
import pandas as pd

conn = sqlite3.connect('Phase1_DataPipeline/zomato.db')
df = pd.read_sql("SELECT name, rate_num, cost_num, location, cuisines FROM restaurants WHERE location LIKE '%Kaggadasapura%' AND cuisines LIKE '%Tamil%'", conn)
print(f"Total matches: {len(df)}")
if len(df) > 0:
    print(df)
