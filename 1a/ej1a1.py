"""
Enunciado:
Introducción básica a la biblioteca requests de Python.
La biblioteca requests permite realizar peticiones HTTP de forma sencilla.

En este ejercicio, aprenderás a:
1. Realizar una petición GET a una API pública
2. Interpretar una respuesta en formato texto plano
3. Manejar errores en peticiones HTTP

Tu tarea es completar la función indicada para realizar una consulta básica
a la API de ipify.org, un servicio estable que proporciona la IP pública.
"""


def get_user_ip():
    """
    Realiza una petición GET a api.ipify.org para obtener la dirección IP pública
    en formato texto plano.

    Returns:
        str: La dirección IP si la petición es exitosa
        None: Si ocurre un error en la petición
    """
    import requests

    try:
        response = requests.get("https://api.ipify.org")
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception:
        return None


if __name__ == "__main__":
    # Ejemplo de uso de la función
    ip = get_user_ip()
    if ip:
        print(f"Tu dirección IP pública es: {ip}")
    else:
        print("No se pudo obtener la dirección IP")
