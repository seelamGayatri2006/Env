from flask import Flask, request, render_template, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)
MODEL_PATH = os.path.join("model", "model.pkl")
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Model not found. Run train_model.py first to create model/model.pkl")

model = joblib.load(MODEL_PATH)

LABELS = {0: "Good", 1: "Moderate", 2: "Unhealthy"}
SUGGESTIONS = {
    "Good": "Air quality is good. No immediate action required. Continue monitoring.",
    "Moderate": "Air quality is moderate. Sensitive groups should reduce prolonged outdoor exertion.",
    "Unhealthy": "Air quality is unhealthy. Avoid outdoor activities, consider masks, and issue alerts."
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json() or request.form
    try:
        # parse inputs (strings -> floats)
        features = [
            float(data.get("PM2_5", 0)),
            float(data.get("PM10", 0)),
            float(data.get("NO2", 0)),
            float(data.get("SO2", 0)),
            float(data.get("CO", 0)),
            float(data.get("Temperature", 25)),
            float(data.get("Humidity", 50))
        ]
    except Exception as e:
        return jsonify({"error": "Invalid input. Ensure numeric values."}), 400

    arr = np.array(features).reshape(1, -1)
    pred = int(model.predict(arr)[0])
    label = LABELS.get(pred, "Unknown")
    suggestion = SUGGESTIONS.get(label, "")
    # probability for class (optional)
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(arr)[0].tolist()
    else:
        probs = []
    return jsonify({
        "prediction": label,
        "prediction_code": pred,
        "probabilities": probs,
        "suggestion": suggestion,
        "inputs": {
            "PM2_5": features[0],
            "PM10": features[1],
            "NO2": features[2],
            "SO2": features[3],
            "CO": features[4],
            "Temperature": features[5],
            "Humidity": features[6]
        }
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
