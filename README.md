# Predictive-Analysis-of-Manufacturing

This Flask API is designed to upload a dataset, train a Logistic Regression model, and make predictions about equipment downtime based on several features.

---

## **Setup and Run Instructions**

### **Prerequisites**
1. **Python:** Ensure Python 3.8 or higher is installed on your system.
2. **Required Libraries:** Install the required libraries using `pip`.
   
### **Installation Steps**
1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv env
   source env/bin/activate   # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask application**:
   ```bash
   python main.py
   ```
   The application will start running on `http://127.0.0.1:8000` by default.

---

## **API Endpoints**

### 1. **Upload Dataset**
   **Endpoint**: `/upload`  
   **Method**: `POST`

   #### Request:
   - Form-data with key `file` and a `.csv` file as the value.

   #### Example Request (using `curl`):
   ```bash
   curl -X POST -F "file=@path/to/your/file.csv" http://127.0.0.1:8000/upload
   ```

   #### Response:
   - Success:
     ```json
     {
       "message": "File uploaded successfully",
       "file_name": "your_file.csv"
     }
     ```
   - Failure:
     ```json
     {
       "error": "No file part in the request"
     }
     ```

---

### 2. **Train the Model**
   **Endpoint**: `/train`  
   **Method**: `POST`

   #### Request:
   No request body is required.

   #### Example Request:
   ```bash
   curl -X POST http://127.0.0.1:8000/train
   ```

   #### Response:
   - Success:
     ```json
     {
       "message": "Model trained successfully",
       "accuracy": 0.85,
       "f1_score": 0.82
     }
     ```
   - Failure:
     ```json
     {
       "error": "No dataset uploaded. Use the /upload endpoint first."
     }
     ```

---

### 3. **Make a Prediction**
   **Endpoint**: `/predict`  
   **Method**: `POST`

   #### Request:
   - JSON body with the following schema:
     ```json
     {
       "Runtime": 5.5,
       "Temperature": 70.2,
       "Vibration": 1.2,
       "Pressure": 101.3,
       "Power_Consumption": 25.0
     }
     ```

   #### Example Request (using `curl`):
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{
       "Runtime": 5.5,
       "Temperature": 70.2,
       "Vibration": 1.2,
       "Pressure": 101.3,
       "Power_Consumption": 25.0
   }' http://127.0.0.1:8000/predict
   ```

   #### Response:
   - Success:
     ```json
     {
       "Downtime": "Yes",
       "Confidence": 0.92
     }
     ```
   - Failure:
     ```json
     {
       "error": "Model not trained. Use the /train endpoint first."
     }
     ```

---

---

## **Testing the API**
1. Use **Postman** or similar API clients to interact with the endpoints.
2. Use the example `curl` commands provided above.

---

## **Error Handling**
The API includes basic error handling to handle the following cases:
- Missing or invalid files in the `/upload` endpoint.
- Model training without uploading a dataset.
- Predictions attempted before model training.

---
