import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import json
import matplotlib.pyplot as plt

# Configurar la página de Streamlit
st.set_page_config(page_title='Sistema de Control Difuso del Clima', layout='wide')

# Definir las variables de entrada difusas con los rangos reales
cloud_cover = ctrl.Antecedent(np.arange(0, 9, 1), 'nubosidad')  # 0 a 8
humidity = ctrl.Antecedent(np.arange(2, 101, 1), 'humedad')     # 2 a 100
pressure = ctrl.Antecedent(np.arange(10, 10512, 1), 'presion')  # 10 a 10511
precipitation = ctrl.Antecedent(np.arange(0, 1001, 1), 'precipitacion')  # 0 a 1000
sunshine = ctrl.Antecedent(np.arange(0, 241, 1), 'horas_sol')   # 0 a 240
temp_mean = ctrl.Antecedent(np.arange(-181, 293, 1), 'temp_media')  # -181 a 292

# Definir la variable de salida (tipo de clima)
weather_type = ctrl.Consequent(np.arange(0, 6, 1), 'tipo_clima')  # Ajuste el rango para más tipos de clima

# Definir funciones de membresía para cada variable de entrada

# Nubosidad
cloud_cover['despejado'] = fuzz.trimf(cloud_cover.universe, [0, 0, 2])
cloud_cover['parcialmente_nublado'] = fuzz.trimf(cloud_cover.universe, [1, 4, 7])
cloud_cover['nublado'] = fuzz.trimf(cloud_cover.universe, [6, 8, 8])

# Humedad
humidity['baja'] = fuzz.trimf(humidity.universe, [2, 2, 40])
humidity['media'] = fuzz.trimf(humidity.universe, [30, 50, 70])
humidity['alta'] = fuzz.trimf(humidity.universe, [60, 100, 100])

# Presión
pressure['baja'] = fuzz.trimf(pressure.universe, [10, 10, 3500])
pressure['normal'] = fuzz.trimf(pressure.universe, [3000, 5500, 8000])
pressure['alta'] = fuzz.trimf(pressure.universe, [7500, 10511, 10511])

# Precipitación
precipitation['ninguna'] = fuzz.trimf(precipitation.universe, [0, 0, 100])
precipitation['ligera'] = fuzz.trimf(precipitation.universe, [50, 200, 350])
precipitation['moderada'] = fuzz.trimf(precipitation.universe, [300, 500, 700])
precipitation['intensa'] = fuzz.trimf(precipitation.universe, [650, 1000, 1000])

# Horas de sol
sunshine['nula'] = fuzz.trimf(sunshine.universe, [0, 0, 60])
sunshine['baja'] = fuzz.trimf(sunshine.universe, [50, 90, 130])
sunshine['media'] = fuzz.trimf(sunshine.universe, [120, 160, 200])
sunshine['alta'] = fuzz.trimf(sunshine.universe, [190, 240, 240])

# Temperatura media
temp_mean['muy_frio'] = fuzz.trimf(temp_mean.universe, [-181, -181, -50])
temp_mean['frio'] = fuzz.trimf(temp_mean.universe, [-60, -20, 20])
temp_mean['templado'] = fuzz.trimf(temp_mean.universe, [10, 50, 90])
temp_mean['calido'] = fuzz.trimf(temp_mean.universe, [80, 292, 292])

# Definir conjuntos difusos para la variable de salida (tipo de clima)
weather_type['lluvioso'] = fuzz.trimf(weather_type.universe, [0, 0, 0])
weather_type['nublado'] = fuzz.trimf(weather_type.universe, [1, 1, 1])
weather_type['frio_humedo'] = fuzz.trimf(weather_type.universe, [2, 2, 2])
weather_type['calido_humedo'] = fuzz.trimf(weather_type.universe, [3, 3, 3])
weather_type['templado'] = fuzz.trimf(weather_type.universe, [4, 4, 4])
weather_type['lluvia_intensa'] = fuzz.trimf(weather_type.universe, [5, 5, 5])

# Mapeo de valores categóricos a términos difusos actualizado
attribute_value_mapping = {
    'cloud_cover_cat': {
        0: 'despejado',
        1: 'parcialmente_nublado',
        2: 'nublado',
        3: 'nublado'
    },
    'humidity_cat': {
        0: 'baja',
        1: 'media',
        2: 'alta',
        3: 'alta'
    },
    'pressure_cat': {
        0: 'baja',
        1: 'normal',
        2: 'alta',
        3: 'alta'
    },
    'precipitation_cat': {
        0: 'ninguna',
        1: 'ligera',
        2: 'moderada',
        3: 'intensa'
    },
    'sunshine_cat': {
        0: 'nula',
        1: 'baja',
        2: 'media',
        3: 'alta'
    },
    'temp_mean_cat': {
        0: 'muy_frio',
        1: 'frio',
        2: 'templado',
        3: 'calido'
    },
    'Clima': {
        'Lluvioso': 'lluvioso',
        'Nublado': 'nublado',
        'Frío Húmedo': 'frio_humedo',
        'Cálido y Húmedo': 'calido_humedo',
        'Templado': 'templado',
        'Lluvia Intensa': 'lluvia_intensa'
    }
}

# Cargar las reglas desde el archivo JSON
with open('prism_rules.json', 'r') as f:
    json_rules = json.load(f)

# Inicializar la lista de reglas
rules = []

# Iterar sobre cada regla en el archivo JSON
for rule in json_rules:
    antecedents = []
    for condition in rule['antecedent']:
        attribute = condition['attribute']
        value = condition['value']
        fuzzy_variable_name = attribute.replace('_cat', '')
        fuzzy_term = attribute_value_mapping[attribute].get(value, None)
        if fuzzy_term is None:
            st.warning(f"Advertencia: {value} no encontrado en {attribute}.")
            continue
        fuzzy_variable = globals()[fuzzy_variable_name]
        antecedents.append(fuzzy_variable[fuzzy_term])

    # Combinar los antecedentes usando el operador AND (&)
    if antecedents:
        antecedent = antecedents[0]
        for a in antecedents[1:]:
            antecedent = antecedent & a
    else:
        antecedent = None

    # Procesar el consecuente
    consequent_attr = rule['consequent']['attribute']
    consequent_value = rule['consequent']['value']
    fuzzy_consequent_term = attribute_value_mapping[consequent_attr].get(consequent_value, None)
    if fuzzy_consequent_term is None:
        st.warning(f"Advertencia: {consequent_value} no encontrado en {consequent_attr}.")
        continue
    fuzzy_consequent = weather_type[fuzzy_consequent_term]

    # Crear la regla
    fuzzy_rule = ctrl.Rule(antecedent, fuzzy_consequent)
    rules.append(fuzzy_rule)

# Crear el sistema de control difuso
weather_ctrl = ctrl.ControlSystem(rules)
weather_simulation = ctrl.ControlSystemSimulation(weather_ctrl)

# Título de la aplicación
st.title("Sistema de Control Difuso del Clima")

# Crear sliders interactivos usando Streamlit
col1, col2 = st.columns(2)

with col1:
    nubosidad = st.slider('Nubosidad', min_value=0, max_value=8, value=4)
    humedad = st.slider('Humedad (%)', min_value=2, max_value=100, value=50)
    presion = st.slider('Presión (hPa)', min_value=10, max_value=10511, value=5000)
with col2:
    precipitacion = st.slider('Precipitación (mm)', min_value=0, max_value=1000, value=0)
    horas_sol = st.slider('Horas de Sol', min_value=0, max_value=240, value=120)
    temp_media = st.slider('Temperatura Media (°C)', min_value=-181, max_value=292, value=15)

# Función para actualizar el sistema difuso y mostrar el resultado
def actualizar_clima(nubosidad, humedad, presion, precipitacion, horas_sol, temp_media):
    weather_simulation.input['nubosidad'] = nubosidad
    weather_simulation.input['humedad'] = humedad
    weather_simulation.input['presion'] = presion
    weather_simulation.input['precipitacion'] = precipitacion
    weather_simulation.input['horas_sol'] = horas_sol
    weather_simulation.input['temp_media'] = temp_media

    weather_simulation.compute()

    tipo_clima_valor = weather_simulation.output['tipo_clima']
    tipo_clima_labels = {
        0: 'Lluvioso',
        1: 'Nublado',
        2: 'Frío Húmedo',
        3: 'Cálido y Húmedo',
        4: 'Templado',
        5: 'Lluvia Intensa'
    }
    tipo_clima_index = int(round(tipo_clima_valor))
    descripcion_clima = tipo_clima_labels.get(tipo_clima_index, 'Indefinido')
    st.subheader("Tipo de clima: " + descripcion_clima)

    # Mostrar el gráfico de la variable de salida
    fig, ax0 = plt.subplots(figsize=(8, 3))
    weather_type.view(sim=weather_simulation, ax=ax0)
    st.pyplot(fig)

# Actualizar y mostrar el resultado
actualizar_clima(nubosidad, humedad, presion, precipitacion, horas_sol, temp_media)
