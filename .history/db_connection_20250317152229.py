import pymysql

# Fonction pour se connecter à la base de données MySQL via pymysql
def get_db_connection():
    try:
        # Connexion à la base de données MySQL
        connection = pymysql.connect(
            host="localhost",  # Serveur local
            user="root",  # Utilisateur MySQL
            password="AbdToufik-mns",  # Mot de passe MySQL
            database="projet"  # Nom de ta base de données
        )
        return connection
    except pymysql.MySQLError as e:
        # Gestion des erreurs de connexion MySQL
        print(f"Erreur de connexion à la base de données MySQL: {e}")
        raise  # On relance l'exception après l'avoir loguée
