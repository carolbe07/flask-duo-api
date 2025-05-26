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
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(image_url, headers=headers)

        if response.status_code != 200:
            return f"❌ Fehler beim Laden des Bildes: Status {response.status_code}", 400

        original = Image.open(BytesIO(response.content)).convert("RGBA")
        original = original.resize((1024, 1024))  # Bildgröße sicherstellen

        # Neues Bild: 2700 x 1024
        result = Image.new("RGBA", (2700, 1024), (255, 255, 255, 255))

        # Berechnete Positionen:
        first_image_position = 100
        second_image_position = first_image_position + 1024 + 452  # 100px + 1024px (erstes Bild) + 452px Abstand
        result.paste(original, (first_image_position, 0))  # Erstes Bild bei 100px
        result.paste(original, (second_image_position, 0))  # Zweites Bild bei 1576px

        # Bild zurückgeben
        output = BytesIO()
        result.save(output, format="PNG")
        output.seek(0)
        return send_file(output, mimetype="image/png")
    except Exception as e:
        return f"❌ Bild konnte nicht verarbeitet werden: {str(e)}", 500
