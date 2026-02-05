# 🚀 Backend Integration Guide - Attendance Risk Prediction

## 📦 Model Files Overview

```
models/
├── logistic_model.pkl       # The main prediction model
├── decision_tree_model.pkl  # Alternative model (even better accuracy)
└── scaler.pkl              # Required for data preprocessing
```

## 🎯 Recommendation: Use the Decision Tree Model

### Why Decision Tree?
- ✅ **Higher accuracy**: 99.9% vs 99.6%
- ✅ **Better for interpretation**: Can show decision rules
- ✅ **More robust**: Handles edge cases better
- ✅ **Faster prediction**: No complex calculations

## 📋 What to Tell Your Backend Developer

### Files to Use:
- `decision_tree_model.pkl` - Main prediction model
- `scaler.pkl` - Required for data preprocessing

### Required Python Libraries:
```python
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
```

## 💻 Sample Integration Code

### Basic Integration
```python
import joblib
import pandas as pd
import numpy as np

class AttendanceRiskPredictor:
    def __init__(self, model_path="models/decision_tree_model.pkl", scaler_path="models/scaler.pkl"):
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
    
    def predict_risk(self, student_data):
        """
        Predict attendance risk for a student
        
        Args:
            student_data (dict): Student data with required fields
            
        Returns:
            dict: Prediction results with risk level
        """
        # Convert to DataFrame
        df = pd.DataFrame([student_data])
        
        # Preprocess the data (same as training)
        # Note: You'll need to implement the same preprocessing steps
        # that were used during training
        
        # Scale the features
        scaled_data = self.scaler.transform(df[feature_columns])
        
        # Make prediction
        prediction = self.model.predict(scaled_data)[0]
        probability = self.model.predict_proba(scaled_data)[0]
        
        # Calculate risk score and level
        risk_score = probability[1] if len(probability) > 1 else probability[0]
        
        if risk_score <= 0.3:
            risk_level = "Low"
        elif risk_score <= 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return {
            "prediction": int(prediction),
            "risk_score": float(risk_score),
            "risk_level": risk_level
        }

# Usage
predictor = AttendanceRiskPredictor()
result = predictor.predict_risk(student_data)
```

### Flask API Integration
```python
from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load models once at startup
model = joblib.load("models/decision_tree_model.pkl")
scaler = joblib.load("models/scaler.pkl")

@app.route('/predict-attendance-risk', methods=['POST'])
def predict_attendance_risk():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = [
            'student_id', 'test_score', 'avg_score_ratio',
            'Week_1_Attendance', 'Week_2_Attendance', 'Week_3_Attendance',
            'Week_4_Attendance', 'Week_5_Attendance', 'Week_6_Attendance',
            'Week_7_Attendance', 'Week_8_Attendance', 'Week_9_Attendance',
            'Week_10_Attendance', 'Week_11_Attendance', 'Week_12_Attendance',
            'Attendance_Decline_Score', 'Average_Attendance'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Convert to DataFrame
        df = pd.DataFrame([data])
        
        # Preprocess data (implement same preprocessing as training)
        # ... preprocessing steps ...
        
        # Scale features
        scaled_data = scaler.transform(df[feature_columns])
        
        # Make prediction
        prediction = model.predict(scaled_data)[0]
        probability = model.predict_proba(scaled_data)[0]
        
        # Calculate risk metrics
        risk_score = probability[1] if len(probability) > 1 else probability[0]
        
        if risk_score <= 0.3:
            risk_level = "Low"
        elif risk_score <= 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return jsonify({
            "success": True,
            "prediction": int(prediction),
            "risk_score": float(risk_score),
            "risk_level": risk_level,
            "student_id": data.get('student_id')
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### FastAPI Integration
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Load models
model = joblib.load("models/decision_tree_model.pkl")
scaler = joblib.load("models/scaler.pkl")

class StudentData(BaseModel):
    student_id: int
    test_score: float
    avg_score_ratio: float
    Week_1_Attendance: float
    Week_2_Attendance: float
    Week_3_Attendance: float
    Week_4_Attendance: float
    Week_5_Attendance: float
    Week_6_Attendance: float
    Week_7_Attendance: float
    Week_8_Attendance: float
    Week_9_Attendance: float
    Week_10_Attendance: float
    Week_11_Attendance: float
    Week_12_Attendance: float
    Attendance_Decline_Score: float
    Average_Attendance: float

class PredictionResponse(BaseModel):
    prediction: int
    risk_score: float
    risk_level: str
    student_id: int

@app.post("/predict-attendance-risk", response_model=PredictionResponse)
async def predict_attendance_risk(student_data: StudentData):
    try:
        # Convert to DataFrame
        df = pd.DataFrame([student_data.dict()])
        
        # Preprocess and scale
        # ... preprocessing steps ...
        scaled_data = scaler.transform(df[feature_columns])
        
        # Predict
        prediction = model.predict(scaled_data)[0]
        probability = model.predict_proba(scaled_data)[0]
        
        risk_score = probability[1] if len(probability) > 1 else probability[0]
        
        if risk_score <= 0.3:
            risk_level = "Low"
        elif risk_score <= 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return PredictionResponse(
            prediction=int(prediction),
            risk_score=float(risk_score),
            risk_level=risk_level,
            student_id=student_data.student_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## 📊 Output Format

### Response Structure:
```json
{
    "prediction": 0,           // 0 (No Risk) or 1 (At Risk)
    "risk_score": 0.85,        // 0.0 to 1.0 (probability of risk)
    "risk_level": "High"       // "Low" (0-0.3), "Medium" (0.3-0.7), "High" (0.7-1.0)
}
```

### Risk Level Interpretation:
- 🟢 **Low Risk (0-0.3)**: Student is performing well, no immediate action needed
- 🟡 **Medium Risk (0.3-0.7)**: Monitor closely, consider gentle interventions
- 🔴 **High Risk (0.7-1.0)**: Immediate intervention required, high priority

## 🔧 Required Input Data Format

### Essential Fields:
```python
required_fields = [
    'student_id',              # Unique student identifier
    'test_score',              # Latest test score
    'avg_score_ratio',         # Average score ratio
    'Week_1_Attendance',       # Attendance percentage for week 1
    'Week_2_Attendance',       # Attendance percentage for week 2
    # ... continue for all 12 weeks
    'Week_12_Attendance',      # Attendance percentage for week 12
    'Attendance_Decline_Score', # Calculated decline score
    'Average_Attendance'       # Overall average attendance
]
```

### Sample Input:
```json
{
    "student_id": 1001,
    "test_score": 85.5,
    "avg_score_ratio": 0.855,
    "Week_1_Attendance": 95.0,
    "Week_2_Attendance": 92.0,
    "Week_3_Attendance": 88.0,
    "Week_4_Attendance": 85.0,
    "Week_5_Attendance": 82.0,
    "Week_6_Attendance": 78.0,
    "Week_7_Attendance": 75.0,
    "Week_8_Attendance": 72.0,
    "Week_9_Attendance": 70.0,
    "Week_10_Attendance": 68.0,
    "Week_11_Attendance": 65.0,
    "Week_12_Attendance": 62.0,
    "Attendance_Decline_Score": 33.0,
    "Average_Attendance": 75.5
}
```

## ⚠️ Important Notes for Backend Developers

### 1. **Data Preprocessing Required**
- The model expects preprocessed data in the same format as training
- You'll need to implement the same feature engineering steps
- Always use the provided `scaler.pkl` for data scaling

### 2. **Model Loading**
- Load models once at application startup
- Don't reload models for each prediction (performance impact)
- Handle model loading errors gracefully

### 3. **Error Handling**
- Validate input data before prediction
- Handle missing or invalid values
- Provide meaningful error messages

### 4. **Performance Considerations**
- Decision Tree model is very fast (milliseconds per prediction)
- Consider caching for frequently accessed student data
- Batch predictions if processing multiple students

### 5. **Model Updates**
- Models should be retrained periodically with new data
- Implement a model versioning system
- Test new models before deploying to production

## 🧪 Testing Your Integration

### Test Cases:
1. **High Risk Student**: Low attendance trend, declining scores
2. **Low Risk Student**: Consistent attendance, good scores
3. **Edge Cases**: Missing data, extreme values
4. **Invalid Input**: Wrong data types, missing required fields

### Sample Test Data:
```python
# High Risk Test Case
high_risk_student = {
    "student_id": 9999,
    "test_score": 45.0,
    "avg_score_ratio": 0.45,
    "Week_1_Attendance": 90.0,
    "Week_2_Attendance": 80.0,
    "Week_3_Attendance": 70.0,
    "Week_4_Attendance": 60.0,
    "Week_5_Attendance": 50.0,
    "Week_6_Attendance": 40.0,
    "Week_7_Attendance": 35.0,
    "Week_8_Attendance": 30.0,
    "Week_9_Attendance": 25.0,
    "Week_10_Attendance": 20.0,
    "Week_11_Attendance": 15.0,
    "Week_12_Attendance": 10.0,
    "Attendance_Decline_Score": 80.0,
    "Average_Attendance": 42.5
}

# Expected: prediction=1, risk_score>0.7, risk_level="High"
```

## 🚀 Quick Start Checklist

- [ ] Copy `decision_tree_model.pkl` and `scaler.pkl` to your project
- [ ] Install required Python packages: `joblib`, `pandas`, `scikit-learn`
- [ ] Implement data preprocessing pipeline
- [ ] Create prediction endpoint
- [ ] Add input validation
- [ ] Test with sample data
- [ ] Deploy and monitor

---

**Need Help?** Check the main `README.md` for detailed training and data preparation instructions.
