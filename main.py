from flask import Flask, request, send_file
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask-API läuft! Nutze /duo?image=https://..."

@app.route("/duo")
def duo():
    image_url = request.args.get("image")
    if not image_url:
        return "❌ Parameter 'image' fehlt", 400
    try:
        # Bild laden
        response = requests.get(image_url)
        original = Image.open(BytesIO(response.content)).convert("RGBA")

        # Zielgröße der Einzelbilder prüfen/anpassen (falls nicht 1024x1024)
        original = original.resize((1024, 1024))

        # Neues leeres Bild (2700x1024)
        result = Image.new("RGBA", (2700, 1024), (255, 255, 255, 255))

        # Erstes Bild bei x = 100
        result.paste(original, (100, 0))

        # Zweites Bild bei x = 1576 (100 + 1024 + 452)
        result.paste(original, (1576, 0))

        # Ausgabe vorbereiten
        output = BytesIO()
        result.save(output, format="PNG")
        output.seek(0)
        return send_file(output, mimetype="image/png")
    except Exception as e:
        return f"Fehler: {str(e)}", 500
