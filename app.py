# Archivo: app.py

import requests
from flask import Flask, render_template, request

# --- Configuración ---
app = Flask(__name__) # Inicializa la aplicación Flask
API_KEY = "3e53876f934b39170197169363778648" # Tu API Key

# --- Función de Lógica (la que ya teníamos) ---
def obtener_clima(ciudad):
    """Obtiene el clima de una ciudad específica desde OpenWeatherMap."""
    URL = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"q={ciudad}&"
        f"appid={API_KEY}&"
        f"units=metric&"
        f"lang=es"
    )
    
    try:
        respuesta = requests.get(URL)
        respuesta.raise_for_status() # Lanza error si la petición falla
        datos_clima = respuesta.json()
        
        # Extraer y organizar los datos que necesitamos
        clima = {
            "ciudad": datos_clima.get("name"),
            "temperatura": datos_clima.get("main", {}).get("temp"),
            "descripcion": datos_clima.get("weather", [{}])[0].get("description", "No disponible"),
            "icono": datos_clima.get("weather", [{}])[0].get("icon"), # Icono del clima
            "error": None
        }
        return clima
    
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            return {"error": f"Ciudad '{ciudad}' no encontrada."}
        else:
            return {"error": f"Error de API: {err}"}
    except Exception as e:
        return {"error": f"Ocurrió un error inesperado: {e}"}

# --- Rutas de la Aplicación Web ---

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Ruta principal. Muestra el formulario (GET) y 
    procesa la solicitud de clima (POST).
    """
    datos_clima = None # Inicializa los datos del clima
    
    # Si el usuario envía el formulario (método POST)...
    if request.method == "POST":
        ciudad = request.form["ciudad"] # Obtiene la ciudad del formulario
        if ciudad:
            datos_clima = obtener_clima(ciudad)
            
    # Muestra la página HTML y le pasa los datos del clima (si existen)
    return render_template("index.html", clima=datos_clima)

# --- Ejecutar la aplicación ---
if __name__ == "__main__":
    app.run(debug=True) # debug=True nos ayuda a ver errores