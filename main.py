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
        # Lade das Hauptbild
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(image_url, headers=headers)

        if response.status_code != 200:
            return f"❌ Fehler beim Laden des Bildes: Status {response.status_code}", 400

        # Lade das Bild und mache es 1024x1024
        original = Image.open(BytesIO(response.content)).convert("RGBA")
        original = original.resize((1024, 1024))  # Bildgröße sicherstellen

        # Lade die Abstands-Bilder
        transparent_100px = Image.open(BytesIO(requests.get("https://res.cloudinary.com/dp83ggvwp/image/upload/v1748257122/100x1024_nlzwnc.png").content))
        transparent_452px = Image.open(BytesIO(requests.get("https://res.cloudinary.com/dp83ggvwp/image/upload/v1748257121/452x1024_bfpu1w.png").content))

        # Neues Bild erstellen (2700 x 1024)
        result = Image.new("RGBA", (2700, 1024), (255, 255, 255, 255))

        # Erstes Bild bei 100px
        result.paste(original, (100, 0))

        # Füge das 100px Abstandbild ein
        result.paste(transparent_100px, (100 + 1024, 0))

        # Füge das zweite Bild nach dem ersten Abstand ein
        result.paste(original, (100 + 1024 + 100, 0))

        # Füge das 452px Abstandbild ein
        result.paste(transparent_452px, (100 + 1024 + 100 + 1024, 0))

        # Füge das zweite Bild nach dem zweiten Abstand ein
        result.paste(original, (100 + 1024 + 100 + 1024 + 452, 0))

        # Füge den 100px Abstand nach dem zweiten Bild ein
        result.paste(transparent_100px, (100 + 1024 + 100 + 1024 + 452 + 1024, 0))

        # Bild zurückgeben
        output = BytesIO()
        result.save(output, format="PNG")
        output.seek(0)
        return send_file(output, mimetype="image/png")
    except Exception as e:
        return f"❌ Bild konnte nicht verarbeitet werden: {str(e)}", 500
