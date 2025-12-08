"""
Enunciado:
Desarrolla un cliente para consultar la información de estaciones del sistema de bicicletas
compartidas de Barcelona utilizando la API GBFS (General Bikeshare Feed Specification).

Tareas:
1. Consultar el endpoint de información de estaciones
2. Extraer datos específicos de cada estación
3. Convertir coordenadas de estaciones a un DataFrame de pandas
4. Procesar y estructurar la información recibida

Esta práctica te ayudará a entender cómo trabajar con APIs reales y procesar datos
en diferentes formatos utilizando pandas.

Tu tarea es completar la implementación de las funciones indicadas.
"""

import pandas as pd
import requests


def get_stations_data():
    """
    Realiza una petición a la API para obtener información de las estaciones
    y extrae el objeto 'data' de la respuesta.

    Returns:
        dict: El objeto 'data' que contiene la lista de estaciones
        None: Si ocurre un error en la petición o el objeto 'data' no existe
    """
    # URL del endpoint de información de estaciones
    url = (
        "https://barcelona.publicbikesystem.net/customer/gbfs/v2/en/station_information"
    )

    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            return json_data.get("data")
        else:
            return None
    except Exception:
        return None


def get_station_info(stations_data, station_id):
    """
    Busca y devuelve la información de una estación específica según su ID.

    Args:
        stations_data (dict): Datos de estaciones obtenidos con get_stations_data()
        station_id (str): ID de la estación a buscar

    Returns:
        dict: Información de la estación solicitada
        None: Si no se encuentra la estación o los datos de entrada son inválidos
    """
    if stations_data is None:
        return None

    stations = stations_data.get("stations", [])
    if not stations:
        return None

    for station in stations:
        if station.get("station_id") == station_id:
            return station

    return None


def get_station_coordinates(station_info):
    """
    Extrae las coordenadas (latitud y longitud) de una estación.

    Args:
        station_info (dict): Información de una estación específica

    Returns:
        tuple: Par (latitud, longitud) de la estación
        None: Si station_info es None o no contiene las coordenadas
    """
    if station_info is None:
        return None

    lat = station_info.get("lat")
    lon = station_info.get("lon")

    if lat is None or lon is None:
        return None

    return (lat, lon)


def create_stations_dataframe(stations_data):
    """
    Crea un DataFrame de pandas con información básica de todas las estaciones.

    Args:
        stations_data (dict): Datos de estaciones obtenidos con get_stations_data()

    Returns:
        pandas.DataFrame: DataFrame con columnas 'station_id', 'latitude', 'longitude', 'name'
        None: Si stations_data es None o no tiene la estructura esperada
    """
    if stations_data is None:
        return None

    stations = stations_data.get("stations")
    if stations is None:
        return None

    data_list = []
    for station in stations:
        data_list.append(
            {
                "station_id": station.get("station_id"),
                "latitude": station.get("lat"),
                "longitude": station.get("lon"),
                "name": station.get("name"),
            }
        )

    return pd.DataFrame(data_list)


if __name__ == "__main__":
    # Obtener los datos de todas las estaciones
    stations_data = get_stations_data()

    if stations_data:
        # Ejemplo: Obtener información de la estación con ID "1"
        station_1 = get_station_info(stations_data, "1")
        if station_1:
            print(f"Estación encontrada: {station_1['name']}")

            # Obtener coordenadas
            coordinates = get_station_coordinates(station_1)
            if coordinates:
                lat, lon = coordinates
                print(f"Coordenadas: ({lat}, {lon})")

        # Crear DataFrame con todas las estaciones
        df = create_stations_dataframe(stations_data)
        if df is not None:
            print("\nPrimeras 5 estaciones:")
            print(df.head())
            print(f"\nTotal de estaciones: {len(df)}")
    else:
        print("No se pudieron obtener los datos de las estaciones.")
