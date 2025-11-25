from flask import Flask, render_template, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Chemin du dossier static/images
    image_folder = os.path.join(app.static_folder, "images")
    images = []

    # Parcourt tous les fichiers du dossier
    for file in os.listdir(image_folder):
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
            images.append("images/" + file)

    return render_template("index.html", images=images)

if __name__ == "__main__":
    app.run(debug=True)

