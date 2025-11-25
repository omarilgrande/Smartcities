# ============================
# FICHIER : appli.py
# Rôle : Serveur Flask pour configurer le Wi-Fi et les paramètres de la caméra ESP32
# ============================

from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# ============================
# PAGE PRINCIPALE "/"
# ============================
@app.route('/')
def index():
    # Récupère les images dans static/images/
    image_folder = os.path.join(app.static_folder, "images")
    images = [
        f"images/{file}" for file in os.listdir(image_folder)
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))
    ]
    return render_template("index.html", images=images)

# ============================
# TRAITEMENT DES PARAMÈTRES ENVOYÉS PAR LE FORMULAIRE
# ============================
@app.route('/update_params', methods=['POST'])
def update_params():
    # Paramètres Wi-Fi
    ssid = request.form.get('ssid')
    password = request.form.get('password')

    # Paramètres caméra
    resolution = request.form.get('resolution')
    brightness = request.form.get('brightness')
    contrast = request.form.get('contrast')
    saturation = request.form.get('saturation')
    quality = request.form.get('quality')
    mirror = request.form.get('mirror')
    flip = request.form.get('flip')

    print("=== PARAMÈTRES REÇUS ===")
    print(f"Wi-Fi SSID : {ssid}")
    print(f"Wi-Fi Mot de passe : {password}")
    print(f"Résolution : {resolution}")
    print(f"Luminosité : {brightness}")
    print(f"Contraste : {contrast}")
    print(f"Saturation : {saturation}")
    print(f"Qualité JPEG : {quality}")
    print(f"Miroir : {mirror}")
    print(f"Rotation : {flip}")
    print("=========================")

    # Exemple d’envoi vers l’ESP32 (à activer plus tard)
    # import requests
    # esp32_url = "http://192.168.1.50/config"
    # requests.post(esp32_url, data=request.form)

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
