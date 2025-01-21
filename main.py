from flask import Flask, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

# Initialize Flask app
app = Flask(__name__)

# Global variables to store data, model, and scaler
data = None
model = None
scaler = None

# Feature columns
FEATURES = ['Runtime', 'Temperature', 'Vibration', 'Pressure', 'Power_Consumption']
TARGET = 'Downtime'


# Route to upload a dataset
@app.route("/upload", methods=["POST"])
def upload_file():
    global data
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    try:
        # Read the CSV file into a DataFrame
        data = pd.read_csv(request.files['file'])
        print(data.head())
        return jsonify({"message": "File uploaded successfully", "file_name": file.filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to train the model
@app.route("/train", methods=["POST"])
def train_model():
    global data, model, scaler

    if data is None:
        return jsonify({"error": "No dataset uploaded. Use the /upload endpoint first."}), 400

    try:
        # Binarize the target variable if needed
        threshold = 5  # Adjust based on your data
        data[TARGET] = (data[TARGET] > threshold).astype(int)

        # Splitting the data
        X = data[FEATURES]
        y = data[TARGET]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Standardize the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train a Logistic Regression model
        model = LogisticRegression(random_state=42)
        model.fit(X_train_scaled, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        return jsonify({
            "message": "Model trained successfully",
            "accuracy": accuracy,
            "f1_score": f1
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to make predictions
@app.route("/predict", methods=["POST"])
def predict():
    global model, scaler

    if model is None or scaler is None:
        return jsonify({"error": "Model not trained. Use the /train endpoint first."}), 400

    try:
        # Extract JSON input
        input_data = request.json
        if not input_data:
            return jsonify({"error": "No input data provided"}), 400

        # Convert input data to DataFrame
        input_df = pd.DataFrame([input_data])

        # Ensure the input data has all required features
        missing_features = [feature for feature in FEATURES if feature not in input_df.columns]
        if missing_features:
            return jsonify({"error": f"Missing features: {missing_features}"}), 400

        # Standardize the input features
        input_scaled = scaler.transform(input_df)

        # Make prediction
        prediction = model.predict(input_scaled)[0]
        confidence = model.predict_proba(input_scaled)[0].max()

        return jsonify({
            "Downtime": "Yes" if prediction == 1 else "No",
            "Confidence": round(confidence, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)
