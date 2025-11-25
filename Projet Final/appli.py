# ============================
# FICHIER : appli.py
# Rôle : Serveur Flask qui affiche toutes les images du dossier static/images
# ============================

# Importation des modules nécessaires
from flask import Flask, render_template, url_for  # Flask = framework web, render_template = affiche HTML, url_for = gère les chemins
import os  # os permet de manipuler le système de fichiers (accéder aux dossiers, lister les fichiers, etc.)

# Création de l'application Flask
app = Flask(__name__)

# ============================
# ROUTE PRINCIPALE "/"
# Cette route est appelée quand on visite http://127.0.0.1:5000/
# ============================
@app.route('/')
def index():
    # On définit le chemin vers le dossier qui contient les images
    # app.static_folder = le dossier "static" par défaut dans Flask
    image_folder = os.path.join(app.static_folder, "images")

    # On crée une liste vide qui contiendra les chemins des images
    images = []

    # On parcourt tous les fichiers présents dans static/images/
    for file in os.listdir(image_folder):
        # On ne garde que les fichiers d'images selon leur extension
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
            # On ajoute le chemin relatif (ex: "images/photo1.png") dans la liste
            images.append("images/" + file)

    # On renvoie la page HTML index.html
    # On lui passe la liste "images" pour qu'elle affiche toutes les images trouvées
    return render_template("index.html", images=images)

# ============================
# Lancement du serveur Flask
# ============================
if __name__ == "__main__":
    # debug=True : recharge automatiquement l'app en cas de modification + affiche les erreurs
    app.run(debug=True)
