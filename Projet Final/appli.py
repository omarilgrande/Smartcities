from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    # Tu peux générer la liste des images automatiquement si tu veux
    images = [
        "images/photo1.PNG",
        "images/photo2.PNG",
        "images/photo3.PNG"
    ]
    return render_template("index.html", images=images)

if __name__ == "__main__":
    app.run(debug=True)
