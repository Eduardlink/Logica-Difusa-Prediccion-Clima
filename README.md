
# Proyecto de Predicción de Clima con Lógica Difusa

Este proyecto utiliza lógica difusa y aprendizaje automático para predecir el clima a partir de datos meteorológicos. A continuación se describen los pasos necesarios para configurar el entorno y las dependencias.

## Requisitos previos

Asegúrate de tener **Python 3** instalado en tu sistema. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).

## Configuración del Entorno Virtual

Sigue los pasos a continuación para configurar el entorno virtual e instalar las librerías necesarias:

### 1. Clonar el repositorio

Si aún no has clonado el repositorio, hazlo con el siguiente comando:

```bash
git clone <URL-del-repositorio>
cd nombre-del-repositorio
```

### 2. Crear el entorno virtual

Ejecuta el siguiente comando para crear un entorno virtual llamado `logica_difusa_env`:

```bash
python -m venv logica_difusa_env
```

### 3. Activar el entorno virtual

- En **Windows**:

  ```bash
  logica_difusa_env\Scripts\activate
  ```

- En **macOS/Linux**:

  ```bash
  source logica_difusa_env/bin/activate
  ```

Una vez activado, deberías ver el nombre del entorno virtual al inicio de tu línea de comandos.

### 4. Instalar las librerías necesarias

Ejecuta los siguientes comandos para instalar las dependencias del proyecto:

```bash
pip install pandas
pip install scikit-learn
pip install numpy
pip install streamlit
pip install scikit-fuzzy
pip install matplotlib
pip install networkx
```

Alternativamente, si tienes un archivo `requirements.txt`, puedes instalar todas las dependencias con:

```bash
pip install -r requirements.txt
```

## Ejecución del Proyecto

Una vez que hayas configurado el entorno y las dependencias, puedes ejecutar el proyecto según tus necesidades. Por ejemplo, si tienes un script principal, ejecuta:

```bash
python nombre_del_script.py
```

O si tienes un archivo específico para iniciar la aplicación (por ejemplo, una aplicación de Streamlit):

```bash
streamlit run nombre_del_archivo.py
```

## Desactivación del Entorno Virtual

Cuando termines de trabajar en el proyecto, puedes desactivar el entorno virtual con el siguiente comando:

```bash
deactivate
```

## Generación de `requirements.txt`

Si actualizas o agregas nuevas librerías, puedes generar un nuevo archivo `requirements.txt` con el siguiente comando:

```bash
pip freeze > requirements.txt
```

Este archivo puede ser utilizado posteriormente para instalar todas las dependencias necesarias con un solo comando (`pip install -r requirements.txt`).

## Estructura del Proyecto

Este es un resumen de la estructura del proyecto:

```
nombre-del-repositorio/
├── logica_difusa_env/       # Entorno virtual (no se incluye en el repositorio)
├── data/                    # Archivos de datos (por ejemplo, weather_prediction.csv)
├── scripts/                 # Código fuente del proyecto
│   ├── cluster.py           # Script para clusterización
│   ├── logicaDifusa.py      # Lógica difusa para predicción
│   ├── prism.py             # Otro script relevante
├── .gitignore               # Archivos y carpetas ignorados por Git
├── librerias.txt            # Lista de librerías necesarias (opcional)
└── README.md                # Instrucciones del proyecto
```

## Notas

- Asegúrate de activar el entorno virtual cada vez que trabajes en el proyecto para garantizar que estás usando las versiones correctas de las librerías.
- Mantén actualizado el archivo `requirements.txt` cada vez que agregues nuevas dependencias al proyecto.

## Autor

Desarrollado por [Tu Nombre].
