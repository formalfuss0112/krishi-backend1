import os
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_db, save_prediction, get_all_predictions


app = Flask(__name__)
CORS(app)  # ✅ Allow CORS so frontend can access
 
openai.api_key = os.environ.get("OPENAI_API_KEY")

init_db()  # ✅ Initialize SQLite database

@app.route("/")
def home():
    return {"message": "Krishi Sakhi Backend is Running!"}

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            temperature=0.7
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        required_fields = ["disease", "advice", "temperature", "humidity", "pH"]
        missing = [field for field in required_fields if field not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

        # Convert to correct types
        disease = data["disease"]
        advice = data["advice"]
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
        ph = float(data["pH"])

        # Save in database
        save_prediction(disease, advice, temperature, humidity, ph)

        return jsonify({
            "disease": disease,
            "advice": advice,
            "temperature": temperature,
            "humidity": humidity,
            "pH": ph
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/history", methods=["GET"])
def history():
    try:
        predictions = get_all_predictions()
        return jsonify(predictions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return {"status": "Backend is healthy", "version": "1.0"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
