import pandas as pd
from sklearn.cluster import KMeans


df = pd.read_csv('weather_prediction.csv') 
columnas = ['cloud_cover', 'humidity', 'pressure', 'precipitation', 'sunshine', 'temp_mean']
n_clusters = 4


def clusterizar_columna(df, columna, n_clusters):
   
    datos = df[[columna]].values.reshape(-1, 1)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(datos)
    df[columna + '_cat'] = kmeans.labels_
    return df


for columna in columnas:
    df = clusterizar_columna(df, columna, n_clusters)

df.to_csv('weather_prediction_clusterizado.csv', index=False)

print("El archivo 'weather_prediction_clusterizado.csv' ha sido generado con éxito.")