import requests
import json
from cassandra.cluster import Cluster

API_KEY = "cbedf9374cc81594a05d3ed33264416a"


# URL de l'API pour les informations météorologiques
#API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"


# Chargement des données des villes depuis le fichier city.list.json
with open("city.list.json", "r", encoding="utf-8") as json_file:
    city_data = json.load(json_file)

# Liste pour stocker les informations météorologiques des villes de France
weather_data = []

# Boucle à travers les villes
for city in city_data:
    if city["country"] == "FR": 
        #print("condition france validé") # Filtrer les villes de France
        city_name = city["name"]
        #print(city_name)
        city_id = city["id"]

        API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"

        # Paramètres pour l'appel à l'API
        params = {
            "q": city_name,
            "appid": API_KEY,
            "units": "metric" 
        }

        # Appel à l'API
        response = requests.get(API_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            #print("appel api reussi")

            # Extraction des informations pertinentes
            weather_info = {
                "city_id": city_id,
                "city_name": city_name,
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "weather_description": data["weather"][0]["description"]               
            }
            print("infos pertinents reussi")

            # Ajout des informations à la liste
            weather_data.append(weather_info)
            #print(weather_data)

# Affichage des informations météorologiques
for info in weather_data:
    print(f"City_id: {info['city_id']}")
    print(f"City: {info['city_name']}")
    print(f"Temperature: {info['temperature']} °C")
    print(f"Humidity: {info['humidity']}")
    print(f"wind_speed: {info['wind_speed']}")
    print(f"Weather Description: {info['weather_description']}")
    print("-" * 30)
    print("méteo")


auth_provider = PlainTextAuthProvider(username='elastic', password='secret')

# Set up a Cluster object with the contact points (IP addresses or hostnames) of the Cassandra nodes
cluster = Cluster(['localhost'])

# Connect to the cluster and create a session
session = cluster.connect() 

#Creation du keyspace
keyspace_stmt = "CREATE KEYSPACE IF NOT EXISTS weather_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}"
session.execute(keyspace_stmt)

# Création du schéma de la table
table_query = """
    CREATE TABLE IF NOT EXISTS weather_data (
        city_id INT PRIMARY KEY,
        City TEXT,
        temperature FLOAT,
        humidity FLOAT,
        speed FLOAT,
        description TEXT
    )
"""
session.execute(table_query) 

# Fermeture de la session et du cluster
session.shutdown()
cluster.shutdown()