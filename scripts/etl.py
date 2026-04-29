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

#tabela produtos
products_df = df[
    ['name', 'category', 'product_type', 'price', 'brand']
].drop_duplicates().reset_index(drop=True)
#criando produtos_ id
products_df['product_id'] = products_df.index + 1

#tabela sizes
df['sizes_list'] = df['size'].str.replace(' ', '').str.split(',')

sizes_df = df[['name', 'sizes_list']].explode('sizes_list')

sizes_df.rename(columns={'sizes_list': 'size'}, inplace=True)

#relacionando produtos e sizes
sizes_df = sizes_df.merge(
    products_df[['product_id', 'name']],
    on='name',
    how='left'
)

sizes_df = sizes_df[['product_id', 'size']]

#salvando arquivos
products_path = BASE_DIR / 'processed' / 'products.csv'
sizes_path = BASE_DIR / 'processed' / 'sizes.csv'

products_df.to_csv(products_path, index=False)
sizes_df.to_csv(sizes_path, index=False)


print(products_df.head())
print(sizes_df.head())

print(products_df.info())
print(sizes_df.info())
print("ETL finalizado ")

