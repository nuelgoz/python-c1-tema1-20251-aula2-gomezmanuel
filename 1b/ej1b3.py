        else:
            # Implementa aquí el manejo de errores para rutas no definidas
            # Debes:
            # 1. Enviar un código de estado 404
            # 2. Establecer el tipo de contenido como "application/json"
            # 3. Devolver un mensaje de error personalizado en formato JSON
            #    que incluya al menos el código de error y un mensaje descriptivo
            #
            # FORMATO DE RESPUESTA DE ERROR:
            #
            # {
            #    "code": 404,
            #    "message": "Recurso [ruta] no encontrado"
            # }
            #
            # Donde [ruta] debe ser sustituido por la ruta solicitada (self.path)
            # Ejemplo: Si se solicita "/api/users", el mensaje sería "Recurso /api/users no encontrado"
            #
            # Nota: Para los nombres de campo también se aceptan variaciones como:
            # - Para el código: "code" o "status"
            # - Para el mensaje: "message", "descripcion" o "detail"
            self.send_response(404) # <--- 1. Enviar código 404
            self.send_header("Content-Type", "application/json") # <--- 2. Tipo de contenido JSON
            self.end_headers()
            error_info = { # <--- 3. Mensaje de error en formato JSON
                "code": 404,
                "message": f"Recurso {self.path} no encontrado" # <--- Incluye la ruta solicitada
            }
            self.wfile.write(json.dumps(error_info).encode()) # <--- Escribir la respuesta