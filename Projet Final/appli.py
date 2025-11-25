# ============================
# FICHIER : appli.py
# Rôle : Serveur Flask avec interface pour configurer un ESP32
# ============================

from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Route principale : affichage des images + paramètres
@app.route('/')
def index():
    # Récupération automatique des images
    image_folder = os.path.join(app.static_folder, "images")
    images = [f"images/{file}" for file in os.listdir(image_folder)
              if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))]
    
    return render_template("index.html", images=images)

# ============================
# Route pour recevoir les paramètres ESP32 depuis le formulaire
# ============================
@app.route('/update_params', methods=['POST'])
def update_params():
    # On récupère les valeurs envoyées depuis le formulaire HTML
    ssid = request.form.get('ssid')
    password = request.form.get('password')
    freq = request.form.get('freq')
    seuil_temp = request.form.get('seuil_temp')
    seuil_hum = request.form.get('seuil_hum')

    # Pour le moment, on affiche dans la console (plus tard : envoi à l’ESP32)
    print("=== PARAMÈTRES REÇUS ===")
    print(f"SSID WiFi : {ssid}")
    print(f"Mot de passe : {password}")
    print(f"Fréquence d’envoi (s) : {freq}")
    print(f"Seuil température : {seuil_temp}")
    print(f"Seuil humidité : {seuil_hum}")
    print("=========================")

    # Tu pourrais ici ajouter un code pour envoyer ces paramètres à l’ESP32
    # via requête HTTP, MQTT ou websocket selon ton setup

    return redirect(url_for('index'))  # Retour à la page principale

if __name__ == "__main__":
    app.run(debug=True)
