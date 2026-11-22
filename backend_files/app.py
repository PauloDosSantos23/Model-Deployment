import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define paths and load our serialized Random Forest model
MODEL_PATH = 'superkart_model_v1_0.joblib'
model = joblib.load(MODEL_PATH)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'healthy',
        'message': 'SuperKart Forecasting API is up and running!'
    })

@app.route('/v1/predict', methods=['POST'])
def predict():
    try:
        # Retrieve the single payload from the request
        data = request.get_json(force=True)

        # Convert payload to a DataFrame row matching training shape
        input_df = pd.DataFrame([data])

        # Make prediction
        prediction = model.predict(input_df)[0]

        return jsonify({
            'status': 'success',
            'prediction': float(prediction)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/v1/predictbatch', methods=['POST'])
def predictbatch():
    try:
        # Check if file is uploaded
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file part in request'}), 400

        file = request.files['file']

        # Read the uploaded CSV file directly into pandas
        input_df = pd.read_csv(file.stream)

        # Generate predictions for all rows
        predictions = model.predict(input_df)

        # Format predictions matching the expected indices
        results = {str(i): float(pred) for i, pred in enumerate(predictions)}

        return jsonify(results)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

if __name__ == '__main__':
    # Run the server inside our upcoming Docker container context on port 7860
    app.run(host='0.0.0.0', port=7860, debug=False)
