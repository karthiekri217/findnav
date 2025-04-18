from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from PIL import Image
import base64
import io
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Set your Gemini API key here
genai.configure(api_key="AIzaSyDbY3znvkWPHXhohHdZk3bmL5lm6JezKPw")

# ✅ Use Gemini 1.5 model (supports vision)
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

@app.route("/")
def home():
    return render_template("index.html")

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

    # ✅ Gemini 1.5 can take question + PIL image directly
    response = model.generate_content([question, image])
    return jsonify({"answer": response.text})

if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

