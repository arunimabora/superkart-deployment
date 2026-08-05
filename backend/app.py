from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

MODEL_PATH = "superkart_sales_model.joblib"
model = joblib.load(MODEL_PATH)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "SuperKart Sales Prediction API is running"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        required_fields = [
            "Product_Weight",
            "Product_Sugar_Content",
            "Product_Allocated_Area",
            "Product_Type",
            "Product_MRP",
            "Store_Id",
            "Store_Establishment_Year",
            "Store_Size",
            "Store_Location_City_Type",
            "Store_Type",
            "Product_Id_Prefix"
        ]

        missing_fields = [
            field for field in required_fields
            if field not in data
        ]

        if missing_fields:
            return jsonify({
                "error": f"Missing fields: {missing_fields}"
            }), 400

        input_data = pd.DataFrame([data])

        prediction = model.predict(input_data)[0]

        return jsonify({
            "predicted_sales": round(float(prediction), 2)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7860
    )