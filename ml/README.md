# 📚 Attendance Risk Prediction System - Beginner's Guide

## 🎯 What This System Does
This system predicts whether students are at risk of declining attendance using machine learning. It analyzes student data including:
- Test scores and performance
- Weekly attendance patterns
- Mentor and parent information
- Historical attendance decline scores

## 📁 Project Structure
```
D:\SIH25102-symmars\ml\
├── code/                           # 🤖 Machine Learning Code
│   ├── test_simple.py             # 🧪 Simple test script
│   ├── try1.py                    # 🎯 Main ML training code
│   └── try2.py                    # 🔧 Additional ML script
├── data/                           # 📊 All CSV data files
│   ├── Weekly_Scores_Institute1.csv
│   ├── Weekly_Scores_Institute2.csv
│   ├── Students_Institute1.csv
│   ├── Students_Institute2.csv
│   ├── Parents_Institute1.csv
│   ├── Parents_Institute2.csv
│   ├── Mentors_Institute1.csv
│   ├── Mentors_Institute2.csv
│   ├── Attendance_Wide_Format_Institute1.csv
│   └── Attendance_Wide_Format_Institute2.csv
├── models/                         # 📦 Trained ML Models
│   ├── logistic_model.pkl         # 🎯 Trained Logistic Regression model
│   ├── decision_tree_model.pkl    # 🌳 Trained Decision Tree model
│   └── scaler.pkl                 # ⚖️ Data scaling model
└── README.md                      # 📖 This guide
```

## 🚀 Step-by-Step Usage Guide

### Step 1: First-Time Setup (Training Models)
```bash
python code/try1.py
```

**What happens:**
1. 📊 Loads all CSV files from the `data/` folder
2. 🔧 Prepares and merges the data
3. 🤖 Trains two machine learning models:
   - **Logistic Regression** (99.6% accuracy)
   - **Decision Tree** (99.9% accuracy)
4. 💾 Saves trained models as `.pkl` files
5. 🎯 Demonstrates prediction on sample data

### Step 2: Using Models for Predictions

#### Method 1: Using the Built-in Function
```python
import pandas as pd
from code.try1 import predict_risk

# Create new student data
new_student = pd.DataFrame({
    'student_id': [999001],
    'student_name': ['John Doe'],
    'mentor_id': [200001],
    'parent_id': [300001],
    'institute_id': [1],
    'test_score': [85],
    'max_score': [100],
    'avg_score_ratio': [0.85],
    'Week_1_Attendance': [95],
    'Week_2_Attendance': [90],
    # ... (all required columns)
})

# Predict risk
results = predict_risk(new_student, model_type="logistic")
print(results[['student_name', 'Risk_Prediction', 'Risk_Score', 'Risk_Level']])
```

#### Method 2: Direct Model Loading (For Backend Integration)
```python
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load trained models
model = joblib.load("models/logistic_model.pkl")
scaler = joblib.load("models/scaler.pkl")

# Prepare your new student data (same format as training)
# ... preprocessing steps ...

# Make prediction
prediction = model.predict(scaled_data)
probability = model.predict_proba(scaled_data)
```

## 📊 Understanding the Output

### Risk Prediction Results
- **Risk_Prediction**: 0 (No Risk) or 1 (At Risk)
- **Risk_Score**: Probability between 0-1 (higher = more risk)
- **Risk_Level**: 
  - 🟢 **Low Risk** (0-0.3): Student is doing well
  - 🟡 **Medium Risk** (0.3-0.7): Monitor closely
  - 🔴 **High Risk** (0.7-1.0): Immediate intervention needed

### Example Output
```
student_name  Risk_Prediction  Risk_Score  Risk_Level
John Doe      0                0.15        Low
Jane Smith    1                0.85        High
Bob Wilson    0                0.25        Low
```

## 🔧 Backend Integration

### For Web Applications (Flask/FastAPI)
```python
from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load models once at startup
model = joblib.load("models/logistic_model.pkl")
scaler = joblib.load("models/scaler.pkl")

@app.route('/predict', methods=['POST'])
def predict_attendance_risk():
    data = request.json
    
    # Convert to DataFrame
    df = pd.DataFrame([data])
    
    # Preprocess (same as training)
    # ... preprocessing code ...
    
    # Predict
    prediction = model.predict(scaled_data)
    probability = model.predict_proba(scaled_data)
    
    return jsonify({
        'risk_prediction': int(prediction[0]),
        'risk_score': float(probability[0][1]),
        'risk_level': 'High' if probability[0][1] > 0.7 else 'Medium' if probability[0][1] > 0.3 else 'Low'
    })

if __name__ == '__main__':
    app.run(debug=True)
```

## 📋 Required Input Data Format

Your new student data must include these columns:
```python
required_columns = [
    'student_id', 'student_name', 'mentor_id', 'parent_id', 'institute_id',
    'test_score', 'max_score', 'avg_score_ratio',
    'Week_1_Attendance', 'Week_2_Attendance', ..., 'Week_12_Attendance',
    'Attendance_Decline_Score', 'Average_Attendance',
    'Lowest_Week_Attendance', 'Highest_Week_Attendance',
    'mentor_name', 'parent_name'
]
```

## 🎯 Key Features

### ✅ What Works Well
- **High Accuracy**: Both models achieve >99% accuracy
- **Fast Prediction**: Models load and predict in milliseconds
- **Easy Integration**: Simple `.pkl` files for backend integration
- **Risk Scoring**: Provides probability scores, not just yes/no

### ⚠️ Important Notes
- **Data Format**: New data must match the training data format exactly
- **Preprocessing**: Always apply the same scaling and encoding as training
- **Model Updates**: Retrain models periodically with new data
- **Categorical Variables**: Names are encoded, so consistent naming is important

## 🆘 Troubleshooting

### Common Issues:
1. **"Model files not found"**: Run `python code/try1.py` first to train models
2. **"Column not found"**: Ensure your input data has all required columns
3. **"Invalid literal for int()"**: Check that attendance values are numeric
4. **Poor predictions**: Verify your data format matches the training data

### Getting Help:
- Check the console output for detailed error messages
- Ensure all CSV files are in the `data/` folder
- Verify trained models are in the `models/` folder
- Verify Python packages are installed: `pandas`, `scikit-learn`, `joblib`

## 🎉 Success Tips
1. **Start Simple**: Use the built-in `predict_risk()` function first
2. **Test with Sample Data**: Always test with known examples
3. **Monitor Performance**: Track prediction accuracy over time
4. **Regular Updates**: Retrain models with fresh data periodically

---

**Happy Predicting! 🚀**
