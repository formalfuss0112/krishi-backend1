from flask import Flask, request, jsonify
from database import init_db, save_prediction, get_all_predictions

app = Flask(__name__)
init_db()  # initialize DB once when app starts

@app.route("/")
def home():
    return {"message": "Krishi Sakhi Backend is Running!"}

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        required_fields = ["disease", "advice", "temperature", "humidity", "pH"]
        missing = [field for field in required_fields if field not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

        disease = data["disease"]
        advice = data["advice"]
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
        ph = float(data["pH"])

        response = {
            "disease": disease,
            "advice": advice,
            "temperature": temperature,
            "humidity": humidity,
            "pH": ph
        }

        save_prediction(disease, advice, temperature, humidity, ph)
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Fix: This route is now outside of predict()
@app.route("/history", methods=["GET"])
def history():
    try:
        predictions = get_all_predictions()
        return jsonify(predictions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
