"""
Enunciado:
Desarrolla un servidor web básico utilizando la biblioteca http.server de Python.
El servidor debe responder a peticiones GET y proporcionar información sobre la IP del cliente.

`GET /ip`: Devuelve la dirección IP del cliente en formato JSON.

Esta es una introducción a los servidores HTTP en Python para entender cómo:
1. Crear una aplicación web básica sin usar frameworks
2. Responder a diferentes rutas en una petición HTTP
3. Procesar encabezados de peticiones HTTP
4. Devolver respuestas en formato JSON

Tu tarea es completar la implementación de la clase MyHTTPRequestHandler.

Nota: Para obtener la IP del cliente, necesitarás examinar los encabezados de la petición HTTP.
Algunos encabezados comunes para esto son: X-Forwarded-For, X-Real-IP o directamente la dirección
del cliente mediante self.client_address.
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Manejador de peticiones HTTP personalizado
    """

    def do_GET(self):
        """
        Método que se ejecuta cuando se recibe una petición GET.

        Rutas implementadas:
        - `/ip`: Devuelve la IP del cliente en formato JSON

        Para otras rutas, devuelve un código de estado 404 (Not Found).
        """
        if self.path == "/ip":
            client_ip = self._get_client_ip()
            response_data = json.dumps({"ip": client_ip})

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(response_data.encode())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def _get_client_ip(self):
        """
        Método auxiliar para obtener la IP del cliente desde los encabezados.
        Debes implementar la lógica para extraer la IP del cliente desde los encabezados
        de la petición o desde la dirección directa del cliente.

        Returns:
            str: La dirección IP del cliente
        """
        # Verificar X-Forwarded-For (común en servidores con proxy)
        x_forwarded_for = self.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()

        # Verificar X-Real-IP
        x_real_ip = self.headers.get("X-Real-IP")
        if x_real_ip:
            return x_real_ip

        # Como último recurso, usar la dirección directa del cliente
        return self.client_address[0]


def create_server(host="localhost", port=8000):
    """
    Crea y configura el servidor HTTP
    """
    server_address = (host, port)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    return httpd


def run_server(server):
    """
    Inicia el servidor HTTP
    """
    print(f"Servidor iniciado en http://{server.server_name}:{server.server_port}")
    server.serve_forever()


if __name__ == "__main__":
    server = create_server()
    run_server(server)
