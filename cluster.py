import pandas as pd
from sklearn.cluster import KMeans

# Load the dataset with the correct separator
df = pd.read_csv('weather_prediction.csv')  # Removed sep parameter

# List of columns to convert
columnas = ['cloud_cover', 'humidity', 'pressure', 'precipitation', 'sunshine', 'temp_mean']

# Number of clusters you want (adjust as needed)
n_clusters = 4

# Function to apply clustering to a column and convert it to categorical
def clusterizar_columna(df, columna, n_clusters):
    # Reshape data for KMeans
    datos = df[[columna]].values.reshape(-1, 1)
    # Apply KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(datos)
    # Assign cluster labels
    df[columna + '_cat'] = kmeans.labels_
    return df

# Apply the function to each column
for columna in columnas:
    df = clusterizar_columna(df, columna, n_clusters)

# Save the modified DataFrame to a new CSV file
df.to_csv('weather_prediction_clusterizado.csv', index=False)

print("El archivo 'weather_prediction_clusterizado.csv' ha sido generado con éxito.")