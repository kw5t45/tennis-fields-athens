import pandas as pd

df = pd.read_csv('dataset_b_with_territories.csv')

# df['municipality'] = df['territory'].map(mapping)
# df['population'] = df['municipality'].map(municipality_population)
# print(df.head(20))
# df.to_csv('data_full.csv')

coords_only = pd.DataFrame({
    "Name": df['territory'],
    "Latitude": df['latitude'],
    "Longitude": df['longitude']
})
coords_only.to_csv('coords_only.csv')
# https://www.citypopulation.de/en/greece/athens/
# https://tennisradar.gr/blog/