
import pandas as pd
import numpy as np
from collections import Counter
from math import log2

# Cargar el dataset
file_path = '../weather-prediction-with-climate-extended.csv'  # Cambia la ruta según tu archivo
data = pd.read_csv(file_path, delimiter=',')
data.columns = data.columns.str.strip()
data = data.drop(columns=['DATE', 'MONTH'], errors='ignore')

# Definir características y la clase objetivo
feature_columns = ['cloud_cover', 'humidity', 'pressure', 
                   'global_radiation', 'precipitation', 'sunshine', 
                   'temp_mean', 'temp_min', 'temp_max']
target_column = 'Clima'  # Columna de clase

X = data[feature_columns]
y = data[target_column]

# Parámetros del algoritmo genético
population_size = 100
num_generations = 1000
mutation_rate = 0.3  # Tasa de mutación inicial
crossover_rate = 0.6  # Tasa de cruce
num_features = len(feature_columns)
population = np.random.randint(2, size=(population_size, num_features))

# Función para calcular la información mutua manualmente
def calculate_mutual_information(feature, target):
    # Obtener la frecuencia conjunta de (feature, target)
    joint_counts = Counter(zip(feature, target))
    total_samples = len(feature)

    # Obtener las frecuencias marginales
    feature_counts = Counter(feature)
    target_counts = Counter(target)

    # Calcular la información mutua
    mutual_info = 0
    for (feat_val, targ_val), joint_count in joint_counts.items():
        # Probabilidades conjunta y marginales
        p_xy = joint_count / total_samples
        p_x = feature_counts[feat_val] / total_samples
        p_y = target_counts[targ_val] / total_samples

        # Sumar al total de información mutua solo si p_xy > 0
        if p_xy > 0:
            mutual_info += p_xy * log2(p_xy / (p_x * p_y))
    return mutual_info

# Calcular la información mutua para cada característica respecto a Clima
info_mutua = [calculate_mutual_information(X[col], y) for col in feature_columns]

# Función de fitness basada en la suma de la información mutua con Clima
def evaluate(individual):
    selected_features = [index for index, bit in enumerate(individual) if bit == 1]

    if len(selected_features) == 0:
        return 0  # Penalizar individuos que no seleccionen ninguna característica

    # Calcular la suma de la información mutua de las características seleccionadas
    fitness_score = np.sum([info_mutua[index] for index in selected_features])

    return fitness_score  # El fitness es la suma de la información mutua

# Función de selección por ruleta 
def roulette_selection(population, fitness_scores):
    total_fitness = np.sum(fitness_scores)
    if total_fitness == 0:  
        selected_index = np.random.randint(len(population))
    else:
        normalized_fitness = fitness_scores / total_fitness
        selected_index = np.random.choice(np.arange(len(population)), p=normalized_fitness)
    return population[selected_index]

# Función de cruce de un punto
def crossover(parent1, parent2):
    if np.random.rand() < crossover_rate:
        point = np.random.randint(1, num_features - 1)
        child1 = np.concatenate([parent1[:point], parent2[point:]])
        child2 = np.concatenate([parent2[:point], parent1[point:]])
        return child1, child2
    else:
        return parent1, parent2

# Función de mutación
def mutate(individual, mutation_rate):
    for i in range(num_features):
        if np.random.rand() < mutation_rate:
            individual[i] = 1 - individual[i]
    return individual

# Ejecución del algoritmo genético
best_overall_fitness = 0
best_overall_features = []

for generation in range(num_generations):
    # Reducir la tasa de mutación a la mitad de las generaciones
    if generation > num_generations // 2:
        mutation_rate = 0.1

    # Calcular el fitness de cada individuo en la población
    fitness_scores = np.array([evaluate(ind) for ind in population])

    # Selección de la siguiente generación
    new_population = []
    while len(new_population) < population_size:
        parent1 = roulette_selection(population, fitness_scores)
        parent2 = roulette_selection(population, fitness_scores)

        # Cruce y mutación
        child1, child2 = crossover(parent1, parent2)
        child1 = mutate(child1, mutation_rate)
        child2 = mutate(child2, mutation_rate)

        new_population.extend([child1, child2])

    # Actualizar la población
    population = np.array(new_population[:population_size])

    # Mejor individuo de la generación actual
    best_fitness = np.max(fitness_scores)
    best_individual = population[np.argmax(fitness_scores)]
    selected_features = [feature_columns[i] for i in range(num_features) if best_individual[i] == 1]

    # Actualizar el mejor individuo global
    if best_fitness > best_overall_fitness:
        best_overall_fitness = best_fitness
        best_overall_features = selected_features

    print(f"Generación {generation + 1}")
    print(f"Mejor fitness de la generación: {best_fitness:.2f}")
    print(f"Características seleccionadas: {selected_features}")

# Resultados finales
print("\nCaracterísticas seleccionadas por el algoritmo genético:", best_overall_features)