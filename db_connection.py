import pymysql
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Fonction pour se connecter à la base de données MySQL via pymysql
def get_db_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Erreur de connexion à la base de données MySQL: {e}")
        raise
