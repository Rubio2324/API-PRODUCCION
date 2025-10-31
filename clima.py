import requests
import json
import os

# --- Configuración de la API ---
# Tu clave API obtenida de OpenWeatherMap
API_KEY = "3e53876f934b39170197169363778648" 
CIUDAD = "Bogota" # Puedes cambiar la ciudad
UNIDADES = "metric" # Para obtener la temperatura en grados Celsius
IDIOMA = "es" # Para obtener la descripción del clima en español

# Construcción de la URL de la petición GET
URL = (
    f"https://api.openweathermap.org/data/2.5/weather?"
    f"q={CIUDAD}&"
    f"appid={API_KEY}&"
    f"units={UNIDADES}&"
    f"lang={IDIOMA}"
)

# --- Función para obtener y procesar el clima ---
def obtener_clima():
    """Realiza la petición a la API y extrae la información mínima requerida."""
    try:
        # Realizar la petición GET a la API
        print(f"Realizando petición a: {URL}")
        respuesta = requests.get(URL)

        # 1. Manejo de errores de la respuesta HTTP
        respuesta.raise_for_status() # Lanza un error para códigos de estado 4xx/5xx

        # 2. Procesar la respuesta JSON
        datos_clima = respuesta.json()

        # 3. Extracción de la información mínima:
        nombre_ciudad = datos_clima.get("name")
        temperatura = datos_clima.get("main", {}).get("temp")
        
        # La descripción del clima está en una lista dentro del campo "weather"
        # Accedemos al primer elemento de la lista y luego al campo "description"
        descripcion = datos_clima.get("weather", [{}])[0].get("description", "No disponible")

        # 4. Retornar la información extraída
        return {
            "ciudad": nombre_ciudad,
            "temperatura": temperatura,
            "descripcion": descripcion
        }

    except requests.exceptions.HTTPError as err:
        print(f"Error HTTP: {err}")
        print("Asegúrate de que la API Key y el nombre de la ciudad sean correctos.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return None

# --- Ejecución y Presentación de Resultados ---
if __name__ == "__main__":
    clima = obtener_clima()

    if clima:
        print("\n--- Resultados de la API ---")
        print(f"Ciudad: {clima['ciudad']}")
        print(f"Temperatura: {clima['temperatura']} °C")
        print(f"Descripción: {clima['descripcion'].capitalize()}")
        print("----------------------------\n")
        