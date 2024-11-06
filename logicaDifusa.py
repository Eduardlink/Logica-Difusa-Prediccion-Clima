import json
import matplotlib.pyplot as plt
import streamlit as st
from collections import Counter

# Membresía para Cloud Cover
def cloud_cover_low(x):
    if x <= 0:
        return 1
    elif 0 < x < 3:
        return (3 - x) / 3
    return 0

def cloud_cover_medium(x):
    if 1 <= x <= 4:
        return (x - 1) / 3
    elif 4 < x <= 6:
        return (6 - x) / 2
    return 0

def cloud_cover_high(x):
    if 5 <= x <= 7:
        return (x - 5) / 2
    elif x > 7:
        return 1
    return 0

# Membresía para Humidity
def humidity_low(x):
    if x <= 2:
        return 1
    elif 2 < x < 64:
        return (64 - x) / 62
    return 0

def humidity_medium(x):
    if 64 <= x <= 77:
        return (x - 64) / 13
    elif 77 < x <= 99:
        return (99 - x) / 22
    return 0

def humidity_high(x):
    if 81 <= x <= 99:
        return (x - 81) / 18
    return 1 if x > 99 else 0

# Membresía para Pressure
def pressure_low(x):
    if x <= 1001:
        return 1
    elif 1001 < x < 1016:
        return (1016 - x) / (1016 - 1001)
    return 0

def pressure_medium(x):
    if 1001 <= x <= 1015:
        return (x - 1001) / (1015 - 1001)
    elif 1015 < x <= 1035:
        return (1035 - x) / (1035 - 1015)
    return 0

def pressure_high(x):
    if 1016 <= x <= 1026:
        return (x - 1016) / 10
    return 1 if x > 1026 else 0

# Membresía para Precipitation
def precipitation_low(x):
    if x <= 1:
        return 1
    elif 1 < x < 131:
        return (131 - x) / 130
    return 0

def precipitation_medium(x):
    if 131 <= x <= 179:
        return (x - 131) / (179 - 131)
    elif 179 < x <= 199:
        return (199 - x) / (199 - 179)
    return 0

def precipitation_high(x):
    if 199 <= x <= 209:
        return (x - 199) / 10
    return 1 if x > 209 else 0

# Membresía para Sunshine
def sunshine_low(x):
    if x <= 1:
        return 1
    elif 1 < x < 59:
        return (59 - x) / 58
    return 0

def sunshine_medium(x):
    if 59 <= x <= 89:
        return (x - 59) / 30
    elif 89 < x <= 99:
        return (99 - x) / 10
    return 0

def sunshine_high(x):
    if 99 <= x <= 140:
        return (x - 99) / 41
    return 1 if x > 140 else 0

# Membresía para Temp Mean
def temp_mean_low(x):
    if x <= 31:
        return 1
    elif 31 < x < 63:
        return (63 - x) / (63 - 31)
    return 0

def temp_mean_medium(x):
    if 63 <= x <= 89:
        return (x - 63) / (89 - 63)
    elif 89 < x <= 99:
        return (99 - x) / (99 - 89)
    return 0

def temp_mean_high(x):
    if 99 <= x <= 140:
        return (x - 99) / 41
    return 1 if x > 140 else 0

# --- Etapa 1: Fuzzificación ---
def fuzzify_inputs(humidity, cloud_cover, pressure, precipitation, sunshine, temp_mean):
    def get_category(value, low_func, medium_func, high_func):
        memberships = {
            0: low_func(value),
            1: medium_func(value),
            2: high_func(value)
        }
        return max(memberships, key=memberships.get)
    
    return {
        "humidity_cat": get_category(humidity, humidity_low, humidity_medium, humidity_high),
        "cloud_cover_cat": get_category(cloud_cover, cloud_cover_low, cloud_cover_medium, cloud_cover_high),
        "pressure_cat": get_category(pressure, pressure_low, pressure_medium, pressure_high),
        "precipitation_cat": get_category(precipitation, precipitation_low, precipitation_medium, precipitation_high),
        "sunshine_cat": get_category(sunshine, sunshine_low, sunshine_medium, sunshine_high),
        "temp_mean_cat": get_category(temp_mean, temp_mean_low, temp_mean_medium, temp_mean_high)
    }

# --- Etapa 2: Inferencia ---
def load_rules(filename):
    with open(filename, "r") as file:
        rules = json.load(file)
    return rules

def infer_consequent(fuzzified_inputs, rules):
    results = []
    for rule in rules:
        match = True
        for antecedent in rule["antecedent"]:
            attr = antecedent["attribute"]
            value = antecedent["value"]
            if fuzzified_inputs.get(attr) != value:
                match = False
                break
        if match:
            results.append(rule["consequent"]["value"])
    return results

# --- Etapa 3: Agregación ---
def aggregate_results(results):
    if not results:
        return "No prediction"
    
    counts = Counter(results)
    predicted_clima = max(counts, key=counts.get)
    return predicted_clima, results

# --- Etapa 4: Defuzzificación ---
clima_values = {
    "Lluvioso": 20,
    "Nublado": 50,
    "Cálido y Húmedo": 80,
    "Templado": 65,
    "Frío Húmedo": 30,
    "Lluvia Intensa": 10
}

def defuzzify_results(results):
    if not results:
        return None
    
    weighted_sum = sum(clima_values[clima] for clima in results)
    total_weight = len(results)
    crisp_value = weighted_sum / total_weight if total_weight > 0 else None
    return crisp_value

# --- Visualización de funciones de membresía ---
# --- Paso 5: Visualización de funciones de membresía ---
def plot_membership_functions():
    fig, axs = plt.subplots(2, 3, figsize=(18, 10))
    
    # Humidity
    x_vals_humidity = list(range(0, 101))
    axs[0, 0].plot(x_vals_humidity, [humidity_low(x) for x in x_vals_humidity], label="Low")
    axs[0, 0].plot(x_vals_humidity, [humidity_medium(x) for x in x_vals_humidity], label="Medium")
    axs[0, 0].plot(x_vals_humidity, [humidity_high(x) for x in x_vals_humidity], label="High")
    axs[0, 0].set_title("Humidity")
    axs[0, 0].set_xlim([0, 100])
    axs[0, 0].set_ylim([0, 1.1])  # Ajuste para más espacio en y
    axs[0, 0].legend()

    # Cloud Cover
    x_vals_cloud = list(range(0, 11))
    axs[0, 1].plot(x_vals_cloud, [cloud_cover_low(x) for x in x_vals_cloud], label="Low")
    axs[0, 1].plot(x_vals_cloud, [cloud_cover_medium(x) for x in x_vals_cloud], label="Medium")
    axs[0, 1].plot(x_vals_cloud, [cloud_cover_high(x) for x in x_vals_cloud], label="High")
    axs[0, 1].set_title("Cloud Cover")
    axs[0, 1].set_xlim([0, 10])
    axs[0, 1].set_ylim([0, 1.1])  # Ajuste para más espacio en y
    axs[0, 1].legend()

    # Pressure
    x_vals_pressure = list(range(950, 1051))
    axs[0, 2].plot(x_vals_pressure, [pressure_low(x) for x in x_vals_pressure], label="Low")
    axs[0, 2].plot(x_vals_pressure, [pressure_medium(x) for x in x_vals_pressure], label="Medium")
    axs[0, 2].plot(x_vals_pressure, [pressure_high(x) for x in x_vals_pressure], label="High")
    axs[0, 2].set_title("Pressure")
    axs[0, 2].set_xlim([950, 1050])
    axs[0, 2].set_ylim([0, 1.1])  # Ajuste para más espacio en y
    axs[0, 2].legend()

    # Precipitation
    x_vals_precip = list(range(0, 301))
    axs[1, 0].plot(x_vals_precip, [precipitation_low(x) for x in x_vals_precip], label="Low")
    axs[1, 0].plot(x_vals_precip, [precipitation_medium(x) for x in x_vals_precip], label="Medium")
    axs[1, 0].plot(x_vals_precip, [precipitation_high(x) for x in x_vals_precip], label="High")
    axs[1, 0].set_title("Precipitation")
    axs[1, 0].set_xlim([0, 300])
    axs[1, 0].set_ylim([0, 1.1])  # Ajuste para más espacio en y
    axs[1, 0].legend()

    # Sunshine
    x_vals_sunshine = list(range(0, 151))
    axs[1, 1].plot(x_vals_sunshine, [sunshine_low(x) for x in x_vals_sunshine], label="Low")
    axs[1, 1].plot(x_vals_sunshine, [sunshine_medium(x) for x in x_vals_sunshine], label="Medium")
    axs[1, 1].plot(x_vals_sunshine, [sunshine_high(x) for x in x_vals_sunshine], label="High")
    axs[1, 1].set_title("Sunshine")
    axs[1, 1].set_xlim([0, 150])
    axs[1, 1].set_ylim([0, 1.1])  # Ajuste para más espacio en y
    axs[1, 1].legend()

    # Temp Mean
    x_vals_temp = list(range(-30, 51))
    axs[1, 2].plot(x_vals_temp, [temp_mean_low(x) for x in x_vals_temp], label="Low")
    axs[1, 2].plot(x_vals_temp, [temp_mean_medium(x) for x in x_vals_temp], label="Medium")
    axs[1, 2].plot(x_vals_temp, [temp_mean_high(x) for x in x_vals_temp], label="High")
    axs[1, 2].set_title("Temp Mean")
    axs[1, 2].set_xlim([-30, 50])
    axs[1, 2].set_ylim([0, 1.1])  # Ajuste para más espacio en y
    axs[1, 2].legend()
    
    for ax in axs.flat:
        ax.set(xlabel="Value", ylabel="Degree of Membership")
    
    plt.tight_layout()
    st.pyplot(fig)


# --- Interfaz interactiva de Streamlit ---
def interactive_prediction(rules):
    st.title("Sistema de Lógica Difusa para Predicción de Clima")

    # Crear sliders para cada variable
    humidity = st.slider("Humidity", 0, 100)
    cloud_cover = st.slider("Cloud Cover", 0, 10)
    pressure = st.slider("Pressure", 950, 1050)
    precipitation = st.slider("Precipitation", 0, 300)
    sunshine = st.slider("Sunshine", 0, 150)
    temp_mean = st.slider("Temp Mean", -30, 50)

    # Etapa 1: Fuzzificación
    fuzzified_inputs = fuzzify_inputs(humidity, cloud_cover, pressure, precipitation, sunshine, temp_mean)
    st.write("Fuzzificación:", fuzzified_inputs)

    # Etapa 2: Inferencia
    results = infer_consequent(fuzzified_inputs, rules)
    st.write("Resultados de Inferencia:", results)
    # Etapa 3: Agregación
    predicted_clima, all_results = aggregate_results(results)
    st.write("Resultado de Agregación (Predicción de Clima):", predicted_clima)
    st.write("Resultados de todas las reglas aplicadas:", all_results)

    # Etapa 4: Defuzzificación
    crisp_value = defuzzify_results(all_results)
    st.write(f"Valor Defuzzificado (Crisp Value): {crisp_value}")

    # Visualizar las funciones de membresía
    st.write("Funciones de Membresía")
    plot_membership_functions()

# --- Ejecutar funciones ---
if __name__ == "__main__":
    # Cargar reglas del archivo JSON
    rules = load_rules("prism_rules.json")

    # Iniciar predicción interactiva con Streamlit
    interactive_prediction(rules)
