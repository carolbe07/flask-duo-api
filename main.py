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
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(image_url, headers=headers)
        if response.status_code != 200:
            return f"❌ Fehler beim Laden des Bildes: Status {response.status_code}", 400

        original = Image.open(BytesIO(response.content)).convert("RGBA")
        original = original.resize((1024, 1024))

        # Obliczenie całkowitej szerokości
        canvas_width = 100 + 1024 + 452 + 1024 + 100
        canvas_height = 1024

        # Stworzenie pustego obrazu
        result = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 255))

        # Wklejanie obrazów
        x1 = 100
        x2 = x1 + 1024 + 452

        result.paste(original, (x1, 0))
        result.paste(original, (x2, 0))

        # Zwrócenie obrazu
        output = BytesIO()
        result.save(output, format="PNG")
        output.seek(0)
        return send_file(output, mimetype="image/png")
    except Exception as e:
        return f"❌ Bild konnte nicht verarbeitet werden: {str(e)}", 500
