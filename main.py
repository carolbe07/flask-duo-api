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
        response = requests.get(image_url)
        original = Image.open(BytesIO(response.content)).convert("RGBA")
        width, height = original.size
        result = Image.new("RGBA", (width * 2 + 200, height), (255, 255, 255, 0))
        result.paste(original, (0, 0))
        result.paste(original, (width + 200, 0))
        output = BytesIO()
        result.save(output, format="PNG")
        output.seek(0)
        return send_file(output, mimetype="image/png")
    except Exception as e:
        return f"Fehler: {str(e)}", 500
