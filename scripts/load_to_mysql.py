from pathlib import Path
import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
products_path = BASE_DIR / 'processed' / 'products.csv'
sizes_path = BASE_DIR / 'processed' / 'sizes.csv'

products_df = pd.read_csv(products_path)
sizes_df = pd.read_csv(sizes_path)

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()

#inserir produtos
for _, row in products_df.iterrows():
    cursor.execute("""
        INSERT INTO products (name, price, product_type, category,brand)
        VALUES (%s, %s, %s, %s, %s)
    """, (row['name'],
          row['price'], 
          row['product_type'],
          row['category'],
          row['brand']
          ))
    #inserir sizes
    for _, row in sizes_df.iterrows():
        cursor.execute("""
        INSERT INTO sizes (product_id, size)
        VALUES (%s, %s)
    """, (
        int(row['product_id']),
        row['size']
    ))
    
    #salvando
    conn.commit()

print("Dados inseridos!")
print(products_df.shape)
print(sizes_df.shape)


cursor.close()
conn.close()
