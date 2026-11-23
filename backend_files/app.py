# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_predictor_api = Flask("SuperKart Predictor")

# Load the trained machine learning model
model = joblib.load("superkart_model_v1_0.joblib")

# Define a route for the home page (GET request)
@superkart_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "SuperKart Forecasting API is up and running!"

# Define an endpoint for single product prediction (POST request)
@superkart_predictor_api.post('/v1/predict')
def predict_superkart():
    """
    This function handles POST requests to the '/v1/predict' endpoint.
    It expects a JSON payload containing product details and returns
    the predicted superkart as a JSON response.
    """
    # Get the JSON data from the request body
    predict_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'product_id_char': predict_data['product_id_char'],
        'product_sugar_content': predict_data['product_sugar_content'],
        'store_size': predict_data['store_size'],
        'store_location_city_type': predict_data['store_location_city_type'],
        'store_type': predict_data['store_type'],
        'product_type_category': predict_data['product_type_category'],
        'product_weight': predict_data['product_weight'],
        'product_mrp': predict_data['product_mrp'],
        'store_age_years': predict_data['store_age_years'],
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction (get predict)
    predicted_predict = model.predict(input_data)[0]

    # Calculate actual predict
    predicted_predict = np.exp(predicted_predict)

    # Convert predicted_predict to Python float
    predicted_predict = round(float(predicted_predict), 2)
    # The conversion above is needed as we convert the model prediction (predict) to actual predict using np.exp, which returns predictions as NumPy float32 values.
    # When we send this value directly within a JSON response, Flask's jsonify function encounters a datatype error

    # Return the actual predict
    return jsonify({'Predicted Predict (in unit)': predicted_predict})


# Define an endpoint for batch prediction (POST request)
@superkart_predictor_api.post('/v1/predictbatch')
def predict_superkart_batch():
    """
    This function handles POST requests to the '/v1/predictbatch' endpoint.
    It expects a CSV file containing product details for multiple products
    and returns the predicted predict as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all products in the DataFrame (get predict)
    predicted_superkart = model.predict(input_data).tolist()

    # Calculate actual predict
    predicted_superkart = [round(float(np.exp(predict)), 2) for predict in predicted_superkart]

    # Create a dictionary of predictions with predict IDs as keys
    predict_ids = input_data['id'].tolist()  # Assuming 'id' is the predict ID column
    output_dict = dict(zip(predict_ids, predicted_superkart))  # Use actual predict

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    superkart_predictor_api.run(debug=True)
