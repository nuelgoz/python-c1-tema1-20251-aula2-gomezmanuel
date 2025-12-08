"""
Enunciado:
Manejo avanzado de errores HTTP con la biblioteca requests de Python.

En este ejercicio, aprenderás a:
1. Realizar peticiones a diferentes URLs que generarán distintos códigos de estado HTTP
2. Diferenciar entre varios tipos de errores HTTP (4xx, 5xx)
3. Manejar redirecciones (códigos 3xx)
4. Extraer información detallada de las respuestas de error
5. Procesar respuestas JSON con información específica sobre el estado

Tu tarea es completar la función request_with_error_handling para manejar adecuadamente
diferentes tipos de respuestas HTTP, incluyendo errores cliente (4xx), errores servidor (5xx)
y redirecciones (3xx).

Nota: El servidor httpstatuses.maor.io devuelve respuestas JSON con la siguiente estructura:

{
    "code": 404,
    "description": "Not Found"
}

Deberás comprobar que el código en el encabezado HTTP coincide con el campo "code"
en el cuerpo JSON y usar el campo "description" para proporcionar información detallada.
"""

import requests


def request_with_error_handling(url):
    """
    Realiza una petición GET a la URL proporcionada y maneja los diferentes tipos de
    respuestas HTTP que puedan ocurrir.

    Args:
        url (str): La URL a la que se realizará la petición

    Returns:
        dict: Un diccionario con la siguiente información:
            - success (bool): True si la petición fue exitosa (código 2xx), False en otro caso
            - status_code (int): El código de estado HTTP
            - is_redirect (bool): True si la respuesta es una redirección (código 3xx)
            - redirect_url (str, opcional): URL de redirección si is_redirect es True
            - error_type (str, opcional): "client_error" para 4xx, "server_error" para 5xx
            - message (str): Un mensaje descriptivo sobre el resultado de la petición
    """
    try:
        response = requests.get(url, allow_redirects=False)
        status_code = response.status_code

        # Intentar obtener la descripción del JSON si está disponible
        try:
            json_data = response.json()
            description = json_data.get("description", "")
        except Exception:
            description = ""

        # Respuestas exitosas (2xx)
        if 200 <= status_code < 300:
            return {
                "success": True,
                "status_code": status_code,
                "is_redirect": False,
                "message": description or "Request successful",
            }

        # Redirecciones (3xx)
        elif 300 <= status_code < 400:
            redirect_url = response.headers.get("Location", "")
            return {
                "success": False,
                "status_code": status_code,
                "is_redirect": True,
                "redirect_url": redirect_url,
                "message": description or "Redirect",
            }

        # Errores del cliente (4xx)
        elif 400 <= status_code < 500:
            return {
                "success": False,
                "status_code": status_code,
                "is_redirect": False,
                "error_type": "client_error",
                "message": description or "Client error",
            }

        # Errores del servidor (5xx)
        elif 500 <= status_code < 600:
            return {
                "success": False,
                "status_code": status_code,
                "is_redirect": False,
                "error_type": "server_error",
                "message": description or "Server error",
            }

    except requests.exceptions.ConnectionError as e:
        return {
            "success": False,
            "status_code": None,
            "is_redirect": False,
            "message": f"connection_error: {str(e)}",
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": None,
            "is_redirect": False,
            "message": f"Error: {str(e)}",
        }


if __name__ == "__main__":
    # Puedes probar tu función con estas URLs:

    # Para probar un error 404 (Not Found)
    print("Probando URL con error 404:")
    result = request_with_error_handling("https://httpstatuses.maor.io/404")
    print(f"Resultado: {result}")

    # Para probar un error 500 (Server Error)
    print("\nProbando URL con error 500:")
    result = request_with_error_handling("https://httpstatuses.maor.io/500")
    print(f"Resultado: {result}")

    # Para probar una redirección 301 (Moved Permanently)
    print("\nProbando URL con redirección 301:")
    result = request_with_error_handling("https://httpstatuses.maor.io/301")
    print(f"Resultado: {result}")

    # Para probar una respuesta exitosa
    print("\nProbando URL con respuesta exitosa:")
    result = request_with_error_handling("https://httpstatuses.maor.io/200")
    print(f"Resultado: {result}")
