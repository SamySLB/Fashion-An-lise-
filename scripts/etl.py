from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
data_path = BASE_DIR / 'data' / 'shein_sample.csv'
processed_path = BASE_DIR / 'processed' / 'shein_clean.csv'

#ingestão
df = pd.read_csv(data_path, encoding='latin1', sep=None, engine='python')

#limpeza
df.columns = df.columns.str.lower()

df.dropna(subset=['price'], inplace=True)

df['price'] = pd.to_numeric(df['price'], errors='coerce')
df.dropna(subset=['price'], inplace=True)

#Transformação

#Tipo de produto
def categorize(name):
    name = str(name).lower()
    
    if 'dress' in name:
        return 'dress'
    elif 'shirt' in name:
        return 'shirt'
    elif 'pants' in name or 'jeans' in name:
        return 'pants'
    elif 'top' in name or 'blouse' in name:
        return 'top'
    else:
        return 'other'

df['product_type'] = df['name'].apply(categorize)

# categoria (mesma lógica)
df['category'] = df['product_type']

#tamanhos de produtos

# garantir string
df['size'] = df['size'].astype(str)

# transformar em lista (caso venha "S,M,L")
df['sizes_list'] = df['size'].str.split(',')

# contar quantidade de tamanhos
df['size_count'] = df['sizes_list'].apply(len)

# classificar variedade
def classify_variety(n):
    if n == 1:
        return 'single_size'
    elif n <= 3:
        return 'low_variety'
    elif n <= 5:
        return 'medium_variety'
    else:
        return 'high_variety'

df['variety_level'] = df['size_count'].apply(classify_variety)

# marca
df['brand'] = df['brand'].astype(str).str.lower()


df = df[
    [
        'name',
        'category',
        'product_type',
        'price',
        'size',
        'size_count',
        'variety_level',
        'brand'
    ]
]



df.to_csv(processed_path, index=False)

print(df.head())
print(df.info())
print(df.describe())
print("ETL finalizado ")

