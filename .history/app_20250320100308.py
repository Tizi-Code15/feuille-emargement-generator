from flask import Flask, render_template, request, send_file
import os
from db_connection import get_db_connection
from excel_generator import generate_excel

app = Flask(__name__)
# Route principale pour afficher le formulaire
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        promotion_id = request.form["promotion_id"]
        start_date = request.form["start_date"]

        # Connexion à la base de données
        conn = get_db_connection()
        cursor = conn.cursor()

        # Récupérer le nom de la promotion à partir de l'ID sélectionné
        cursor.execute("SELECT nom FROM promotions WHERE id = %s", (promotion_id,))
        promotion_name = cursor.fetchone()[0]  # Récupérer le nom de la promotion

        # Récupérer les stagiaires de la promotion sélectionnée
        cursor.execute("SELECT nom, prenom FROM stagiaires WHERE promotion_id = %s", (promotion_id,))
        stagiaires = cursor.fetchall()

        # Debug: Affichage des stagiaires récupérés
        print(f"Nombre de stagiaires récupérés : {len(stagiaires)}")
        print(stagiaires)  # Affiche tous les stagiaires récupérés

        # Générer le fichier Excel en passant le nom de la promotion
        modified_file_path = generate_excel(promotion_name, start_date, stagiaires)

        # Fermer la connexion à la base de données
        cursor.close()
        conn.close()

        # Afficher un message de succès avec le lien de téléchargement
        return render_template('admin_interface.html', promotions=[], filename=modified_file_path)

    else:
        # Connexion à la base de données pour récupérer les promotions
        conn = get_db_connection()
        cursor = conn.cursor()

        # Récupérer les promotions
        cursor.execute("SELECT id, nom FROM promotions")
        promotions = cursor.fetchall()

        # Fermer la connexion
        cursor.close()
        conn.close()

        return render_template('admin_interface.html', promotions=promotions)

# Route pour télécharger le fichier généré
@app.route("/download/<filename>")
def download(filename):
    # Construire le chemin absolu vers le fichier dans 'generated_files'
    file_path = os.path.join("generated_files", filename)
    
    # Vérifier si le fichier existe avant de le renvoyer
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "Le fichier n'existe pas", 404

if __name__ == "__main__":
    app.run(debug=True)
