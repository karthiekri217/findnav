from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from PIL import Image
import base64
import io
import google.generativeai as genai
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Gemini API setup
genai.configure(api_key="AIzaSyA0KoGY72WO5Xk-_hcJGVR4qFQ0UxdxTW0")
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<page>.html")
def html_page(page):
    try:
        return render_template(f"{page}.html")
    except:
        return "Page not found", 404

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    image_data = data["image"]
    question = data["question"]

    try:
        image_bytes = base64.b64decode(image_data.split(",")[1])
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        return jsonify({"error": f"Image decode failed: {str(e)}"}), 400

    response = model.generate_content([question, image])
    return jsonify({"answer": response.text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
