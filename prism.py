import pandas as pd
import numpy as np
import json  # Importamos el módulo json para manejar archivos JSON

# Paso 1: Cargar el dataset clusterizado
df = pd.read_csv('weather_prediction_clusterizado.csv', sep=',')

# Paso 2: Preparar los datos
columnas_cat = ['cloud_cover_cat', 'humidity_cat', 'pressure_cat',
                'precipitation_cat', 'sunshine_cat', 'temp_mean_cat']
df_cat = df[columnas_cat + ['Clima']]

# Asegurarse de que los valores sean serializables
df_cat = df_cat.applymap(lambda x: x.item() if isinstance(x, (np.int64, np.float64)) else x)

# Paso 3: Definir la función PRISM
def prism(df, class_attr):
    rules = []
    classes = df[class_attr].unique()
    # Iterar sobre cada clase objetivo
    for target_class in classes:
        df_class = df.copy()
        # Continuar hasta que todas las instancias de la clase objetivo estén cubiertas
        while not df_class[df_class[class_attr] == target_class].empty:
            rule_conditions = []
            df_rule = df_class.copy()
            # Construir la regla
            while True:
                max_prob = 0
                best_condition = None
                for attr in columnas_cat:
                    if attr in [cond[0] for cond in rule_conditions]:
                        continue  # Evitar reutilizar el mismo atributo
                    for val in df[attr].unique():
                        # Crear una condición temporal
                        temp_conditions = rule_conditions + [(attr, val)]
                        # Filtrar el dataset basado en las condiciones temporales
                        df_temp = df_rule.copy()
                        for condition in temp_conditions:
                            df_temp = df_temp[df_temp[condition[0]] == condition[1]]
                        if df_temp.empty:
                            continue
                        # Calcular la probabilidad de la clase objetivo
                        num_target_class = len(df_temp[df_temp[class_attr] == target_class])
                        prob = num_target_class / len(df_temp)
                        if prob > max_prob:
                            max_prob = prob
                            best_condition = (attr, val)
                # Añadir la mejor condición a la regla
                if best_condition:
                    rule_conditions.append(best_condition)
                    # Filtrar el dataset para la siguiente iteración
                    df_rule = df_rule[df_rule[best_condition[0]] == best_condition[1]]
                    # Si la regla es 100% precisa, detener
                    if max_prob == 1.0 or len(df_rule[df_rule[class_attr] != target_class]) == 0:
                        break
                else:
                    break  # No se pueden añadir más condiciones
            # Añadir la regla a la lista de reglas
            rules.append((rule_conditions, target_class))
            # Eliminar las instancias cubiertas por la regla
            df_covered = df_class.copy()
            for condition in rule_conditions:
                df_covered = df_covered[df_covered[condition[0]] == condition[1]]
            # Eliminar las instancias cubiertas de la clase objetivo
            df_class = df_class.drop(df_covered[df_covered[class_attr] == target_class].index)
    return rules

# Paso 4: Ejecutar el algoritmo PRISM
rules = prism(df_cat, 'Clima')

# Paso 5: Mostrar las reglas generadas
print("Reglas Generadas por PRISM:")
rule_number = 0
for rule_conditions, target_class in rules:
    rule_number += 1
    antecedent = ' AND '.join([f"{attr}={val}" for attr, val in rule_conditions])
    print(f"Regla {rule_number}: SI {antecedent} ENTONCES Clima={target_class}")
    print("-" * 50)

# Paso 6: Guardar las reglas en un archivo JSON
# Convertir las reglas a un formato serializable
rules_json = []
for rule_conditions, target_class in rules:
    rule_dict = {
        "antecedent": [{ "attribute": str(attr), "value": int(val) if isinstance(val, (np.int64, np.int32)) else str(val) } for attr, val in rule_conditions],
        "consequent": { "attribute": "Clima", "value": str(target_class) }
    }
    rules_json.append(rule_dict)

# Guardar en un archivo JSON
with open('prism_rules.json', 'w', encoding='utf-8') as f:
    json.dump(rules_json, f, ensure_ascii=False, indent=4)

print("Las reglas han sido guardadas en el archivo 'prism_rules.json'.")

# Opcional: Aplicar las reglas al conjunto de datos y calcular la precisión
def apply_rules(rules, df):
    predictions = []
    for index, row in df.iterrows():
        predicted = False
        for rule_conditions, target_class in rules:
            match = True
            for attr, val in rule_conditions:
                if row[attr] != val:
                    match = False
                    break
            if match:
                predictions.append(target_class)
                predicted = True
                break
        if not predicted:
            predictions.append(None)  # Sin predicción
    return predictions

# Aplicar las reglas al dataset
df_cat['Predicción'] = apply_rules(rules, df_cat)

# Calcular la precisión
accuracy = (df_cat['Clima'] == df_cat['Predicción']).mean()
print(f"Precisión de las reglas: {accuracy:.2f}")
