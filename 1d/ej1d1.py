"""
Enunciado:
Este ejercicio introduce el uso de bibliotecas especializadas para acceder a APIs de forma
sencilla y estructurada. En concreto, utilizaremos la biblioteca pybikes que proporciona
wrappers para múltiples sistemas de bicicletas compartidas en todo el mundo.

En lugar de construir nuestro propio cliente HTTP y procesar manualmente los datos JSON,
aprenderemos a utilizar herramientas existentes que hacen este trabajo por nosotros.

Tareas:
1. Explorar los sistemas de bicicletas disponibles
2. Obtener información sobre el sistema de Barcelona (Bicing)
3. Analizar los datos de las estaciones

Esta práctica ilustra cómo las bibliotecas especializadas simplifican el acceso a APIs
y permiten concentrarse en el análisis de datos en lugar de en los detalles técnicos
de la comunicación con la API.
"""

import sys
import time
from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
import pandas as pd
import pybikes


def listar_sistemas_disponibles() -> List[str]:
    """
    Obtiene una lista de todos los sistemas de bicicletas disponibles en pybikes.

    Returns:
        List[str]: Lista de identificadores de sistemas disponibles
    """
    try:
        return list(pybikes.get_all_data().keys())
    except Exception:
        return []


def buscar_sistema_por_ciudad(ciudad: str) -> List[str]:
    """
    Busca sistemas de bicicletas que contengan el nombre de la ciudad especificada.

    Args:
        ciudad (str): Nombre de la ciudad a buscar

    Returns:
        List[str]: Lista de sistemas que coinciden con la búsqueda
    """
    try:
        all_data = pybikes.get_all_data()
        resultados = []
        ciudad_lower = ciudad.lower()
        for tag, info in all_data.items():
            # Buscar en city o en el nombre del sistema
            system_city = info.get("city", "").lower()
            system_name = info.get("name", "").lower()
            if ciudad_lower in system_city or ciudad_lower in system_name:
                resultados.append(tag)
        return resultados
    except Exception:
        return []


def obtener_info_sistema(tag: str) -> Dict[str, Any]:
    """
    Obtiene la información del sistema especificado.

    Args:
        tag (str): Identificador del sistema (por ejemplo, 'bicing')

    Returns:
        Dict[str, Any]: Metadatos del sistema o None si no existe
    """
    try:
        all_data = pybikes.get_all_data()
        if tag in all_data:
            return all_data[tag]
        return None
    except Exception:
        return None


def obtener_estaciones(tag: str) -> Optional[List]:
    """
    Obtiene la lista de estaciones del sistema especificado.

    Args:
        tag (str): Identificador del sistema (por ejemplo, 'bicing')

    Returns:
        Optional[List]: Lista de objetos estación o None si hay error
    """
    try:
        sistema = pybikes.get(tag)
        sistema.update()
        return sistema.stations
    except Exception:
        return None


def crear_dataframe_estaciones(estaciones: List) -> pd.DataFrame:
    """
    Convierte la lista de estaciones en un DataFrame de pandas.

    Args:
        estaciones (List): Lista de objetos estación

    Returns:
        pd.DataFrame: DataFrame con la información de las estaciones
    """
    if not estaciones:
        return pd.DataFrame(columns=["name", "latitude", "longitude", "bikes", "free"])

    data = []
    for estacion in estaciones:
        data.append(
            {
                "name": estacion.name,
                "latitude": estacion.latitude,
                "longitude": estacion.longitude,
                "bikes": estacion.bikes,
                "free": estacion.free,
            }
        )
    return pd.DataFrame(data)


def visualizar_estaciones(df: pd.DataFrame) -> None:
    """
    Genera una visualización simple de la disponibilidad de bicicletas.

    Args:
        df (pd.DataFrame): DataFrame con la información de las estaciones
    """
    if df.empty:
        return

    # Ordenar por bicicletas disponibles y tomar las 10 primeras
    top_10 = df.nlargest(10, "bikes")

    # Crear gráfico de barras
    plt.figure(figsize=(12, 6))
    plt.barh(top_10["name"], top_10["bikes"], color="steelblue")
    plt.xlabel("Bicicletas disponibles")
    plt.ylabel("Estación")
    plt.title("Top 10 estaciones con más bicicletas disponibles")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Listar sistemas disponibles
    print("\nSistemas de bicicletas disponibles:")
    sistemas = listar_sistemas_disponibles()
    print(f"Total: {len(sistemas)} sistemas")
    print(f"Algunos ejemplos: {sistemas[:5]}")

    # Buscar sistemas en Barcelona
    print("\nBuscando sistemas en Barcelona:")
    sistemas_barcelona = buscar_sistema_por_ciudad("Barcelona")
    print(f"Encontrados: {len(sistemas_barcelona)}")
    for sistema in sistemas_barcelona:
        print(f"- {sistema}")

    # Si se encuentra el sistema de Barcelona (Bicing), obtener información
    if "bicing" in sistemas:
        print("\nInformación del sistema Bicing de Barcelona:")
        info = obtener_info_sistema("bicing")
        for key, value in info.items():
            print(f"{key}: {value}")

        # Obtener estaciones
        print("\nObteniendo estaciones...")
        estaciones = obtener_estaciones("bicing")
        if estaciones:
            print(f"Obtenidas {len(estaciones)} estaciones")

            # Convertir a DataFrame
            print("\nConvirtiendo a DataFrame...")
            df = crear_dataframe_estaciones(estaciones)
            print(df.head())

            # Estadísticas básicas
            print("\nEstadísticas de bicicletas disponibles:")
            print(df["bikes"].describe())

            # Visualización
            print("\nVisualizando estaciones con más bicicletas disponibles...")
            visualizar_estaciones(df)
        else:
            print("No se pudieron obtener las estaciones.")
    else:
        print("El sistema 'bicing' no está disponible en pybikes.")
