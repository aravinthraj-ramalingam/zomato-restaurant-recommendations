import pandas as pd
from datasets import load_dataset
import sqlite3
import os

def load_and_inspect():
    dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation")
    df = dataset['train'].to_pandas()
    print(df.head())
    print()
    print("Columns:", df.columns.tolist())
    print()
    print(df.info())

if __name__ == "__main__":
    load_and_inspect()
