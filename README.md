# Tariff Plan Recommendation System

A machine learning-powered tariff plan recommendation system that uses K-means clustering to suggest the top 3 most suitable plans based on user preferences and usage patterns.

## Features

- **Phone-based Login**: Users can login using their phone number to see personalized recommendations
- **ML-Powered Recommendations**: Uses K-means clustering and euclidean distance to find similar usage patterns
- **Interactive Dashboard**: Modern web interface showing current plan, recommendations, and all available plans
- **Real-time Prediction**: Test the prediction system with custom usage parameters
- **Customer Support Chat**: Built-in chatbot for customer queries
- **REST API**: Complete API endpoints for integration
- **Dark Mode Support**: Improved text contrast and visibility in both light and dark themes

## Project Structure

```
last_try/
├── backend.py              # Flask backend server
├── init_db.py             # Database initialization script
├── README.md              # This file
├── artifacts/             # ML model and data artifacts
│   ├── features.json      # Feature names for ML model
│   ├── kmeans.pkl        # Trained K-means model
│   ├── scaler.pkl        # Data scaler for preprocessing
│   └── plan_catalog.csv  # Plan details with pricing
├── frontend/
│   └── index.html        # Frontend HTML file
├── static/
│   └── app.js           # Frontend JavaScript
├── templates/
│   └── index.html       # Alternative frontend template
└── telecom.db          # SQLite database
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### 2. Install Dependencies

```bash
pip3 install flask flask-cors pandas numpy scikit-learn joblib
```

**Required Package Versions:**
```
flask==3.1.2
flask-cors==6.0.1
pandas==2.2.3
numpy==2.2.3
scikit-learn==1.7.2
joblib==1.5.2
```

### 3. Navigate to Project Directory

```bash
cd /Users/xyz/tariff-plan-recommendation
```

### 4. Run the Backend Server

```bash
python3 backend.py
```

The server will start on `http://localhost:5001` with debug mode enabled.

## Usage

### 1. Access the Web Interface

Open your browser and navigate to:
```
http://localhost:5001
```

### 2. Login with Sample Phone Numbers

Try these sample phone numbers to test the system:
- `382-4657` (Basic Plan user - Light usage)
- `358-1921` (Night Owl Premium user - High night usage)  
- `350-8884` (Premium Evening user - High evening usage)

### 3. View Recommendations

After login, you'll see:
- Your current tariff plan
- Top 3 recommended plans based on your usage pattern
- All available plans
- A prediction test tool

### 4. Test Custom Predictions

Use the "KMeans Prediction Test" section to test recommendations with custom usage parameters.

### 5. Customer Support Chat

Click the chat icon in the bottom-right corner to access the customer support chatbot.

## API Documentation

### Base URL
```
http://localhost:5001
```

### Endpoints

#### 1. Main Web Interface
- **Endpoint**: `GET /`
- **Description**: Serves the main web interface
- **Response**: HTML page

#### 2. User Authentication
- **Endpoint**: `POST /api/login`
- **Description**: Login with phone number to get personalized recommendations
- **Request Body**:
  ```json
  {
    "phone": "382-4657"
  }
  ```
- **Response**:
  ```json
  {
    "phone": "382-4657",
    "current_plan": {
      "plan_id": 0,
      "name": "Basic Plan",
      "price": 299.0,
      "centroid": "..."
    },
    "recommendations": [
      {
        "plan_id": 6,
        "name": "Light User",
        "price": 199.0,
        "distance": 0.455,
        "centroid": {...}
      }
    ]
  }
  ```

#### 3. Custom Predictions
- **Endpoint**: `POST /api/predict`
- **Description**: Get recommendations for custom usage patterns
- **Request Body**:
  ```json
  {
    "Day Mins": 200,
    "Eve Mins": 150,
    "Night Mins": 100,
    "Intl Mins": 20,
    "CustServ Calls": 2
  }
  ```
- **Response**:
  ```json
  {
    "recommendations": [
      {
        "plan_id": 0,
        "name": "Basic Plan",
        "price": 299.0,
        "distance": 0.223,
        "centroid": {...}
      }
    ]
  }
  ```

#### 4. All Plans
- **Endpoint**: `GET /api/plans`
- **Description**: Get all available tariff plans
- **Response**:
  ```json
  {
    "plans": [
      {
        "plan_id": 0,
        "name": "Basic Plan",
        "price": 299.0,
        "centroid": "..."
      }
    ]
  }
  ```

## API Testing Examples

### Test Login
```bash
curl -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{"phone": "382-4657"}'
```

### Test Custom Predictions
```bash
curl -X POST http://localhost:5001/api/predict \
  -H "Content-Type: application/json" \
  -d '{"Day Mins": 200, "Eve Mins": 150, "Night Mins": 100, "Intl Mins": 20, "CustServ Calls": 2}'
```

### Get All Plans
```bash
curl http://localhost:5001/api/plans
```

## Sample Data

The system includes sample customers with different usage patterns:

| Phone     | Plan           | Usage Pattern        |
|-----------|----------------|---------------------|
| 382-4657  | Basic Plan     | Light usage         |
| 358-1921  | Night Owl Premium | High night usage |
| 350-8884  | Premium Evening   | High evening usage |

## Machine Learning Model

The recommendation system uses:
- **K-means Clustering**: Groups similar usage patterns into 15 clusters
- **Feature Engineering**: Uses Day/Evening/Night/International minutes and customer service calls
- **Distance Calculation**: Euclidean distance to find closest cluster centroids
- **Preprocessing**: StandardScaler for feature normalization

### Features Used:
1. Day Minutes
2. Evening Minutes  
3. Night Minutes
4. International Minutes
5. Customer Service Calls
6. Total Usage (calculated)

## Available Plans

| Plan ID | Plan Name | Price (₹) | Target Usage |
|---------|-----------|-----------|--------------|
| 0 | Basic Plan | 299 | Light users |
| 1 | Premium Evening | 799 | Heavy evening usage |
| 2 | Night Owl Premium | 999 | Heavy night usage |
| 3 | Business Unlimited | 1299 | Heavy day usage |
| 4 | Standard Evening | 499 | Moderate evening usage |
| 5 | International Plus | 699 | High international calls |
| 6 | Light User | 199 | Very light usage |
| 7 | Balanced Plan | 399 | Balanced usage |
| 8 | Night Basic | 349 | Light night usage |
| 9 | Night Standard | 549 | Moderate night usage |
| 10 | All-Time Starter | 449 | General usage |
| 11 | Night Plus | 599 | Premium night usage |
| 12 | Economy Plan | 249 | Budget users |
| 13 | Night Special | 479 | Special night rates |
| 14 | Weekend Night | 429 | Weekend focused |

## Troubleshooting

### Common Issues

1. **Module not found errors**: Ensure dependencies are installed
   ```bash
   pip3 install flask flask-cors pandas numpy scikit-learn joblib
   ```

2. **Port 5000 conflicts**: The app runs on port 5001 to avoid macOS AirPlay conflicts

3. **Database errors**: Run `python3 init_db.py` to recreate the database

4. **CORS errors**: Flask-CORS is enabled for frontend communication

### Debug Mode

The backend runs in debug mode by default, providing:
- Detailed error messages
- Auto-reload on code changes
- Interactive debugger

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite (lightweight SQL database)
- **Machine Learning**: scikit-learn, pandas, numpy
- **Frontend**: HTML5, JavaScript (ES6+), Tailwind CSS
- **Data Processing**: pandas, joblib for model serialization
- **API**: RESTful APIs with JSON responses

## Features in Detail

### 1. Personalized Recommendations
- Analyzes user's historical usage patterns
- Finds similar users using K-means clustering
- Returns top 3 most suitable plans with similarity scores

### 2. Real-time Predictions
- Test recommendations with any usage combination
- Instant ML predictions without database lookup
- Useful for "what-if" scenarios

### 3. Modern UI/UX
- Responsive design works on all devices
- Dark mode support with improved contrast
- Interactive dashboard with smooth transitions
- Customer support chatbot

### 4. Production Ready
- Error handling and validation
- CORS enabled for API access
- Structured logging and debugging
- Scalable database design

## License

This project is for educational/demonstration purposes.
