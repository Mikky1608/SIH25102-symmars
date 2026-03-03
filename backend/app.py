from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import os
import sys

# Fix Unicode output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Add the ml directory to the path to import the prediction function
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'notifications'))

# Import email service - Resend API only
try:
    from email_service import email_service
    EMAIL_SERVICE_AVAILABLE = True
    EMAIL_SERVICE_TYPE = "Gmail SMTP"
    print(f"[OK] Email service loaded: Gmail SMTP")
    print(f"[INFO] API Key: {'Configured' if email_service.api_key else 'Not set'}")
except Exception as e:
    print(f"[ERROR] Email service error: {e}")
    EMAIL_SERVICE_AVAILABLE = False
    EMAIL_SERVICE_TYPE = "None"
    email_service = None

app = Flask(__name__)
CORS(app)

# Load models once at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'ml', 'models')
try:
    decision_tree_model = joblib.load(os.path.join(MODEL_PATH, 'decision_tree_model.pkl'))
    logistic_model = joblib.load(os.path.join(MODEL_PATH, 'logistic_model.pkl'))
    scaler = joblib.load(os.path.join(MODEL_PATH, 'scaler.pkl'))
    print("[OK] Models loaded successfully!")
except Exception as e:
    print(f"[ERROR] Error loading models: {e}")
    decision_tree_model = None
    logistic_model = None
    scaler = None

class AttendanceRiskPredictor:
    def __init__(self):
        self.decision_tree_model = decision_tree_model
        self.logistic_model = logistic_model
        self.scaler = scaler
    
    def predict_risk(self, student_data, model_type="decision_tree"):
        """Predict attendance risk for a student"""
        try:
            # Convert to DataFrame
            df = pd.DataFrame([student_data])
            
            # Basic preprocessing - encode categorical variables if present
            categorical_cols = ['student_name', 'mentor_name', 'parent_name']
            for col in categorical_cols:
                if col in df.columns:
                    df[col] = df[col].astype(str)
                    # Simple encoding for demo - in production, use saved encoders
                    df[col] = pd.Categorical(df[col]).codes
            
            # Fill missing values
            df = df.fillna(0)
            
            # Drop ID columns for prediction
            drop_cols = ['student_id', 'mentor_id', 'parent_id', 'institute_id']
            feature_cols = [col for col in df.columns if col not in drop_cols]
            X = df[feature_cols]
            
            # Ensure we have the right number of features (adjust as needed)
            # This is a simplified version - in production, ensure exact feature matching
            
            # Select model
            model = self.decision_tree_model if model_type == "decision_tree" else self.logistic_model
            
            if model is None:
                raise Exception("Model not loaded")
            
            # For this demo, we'll use a simplified prediction based on key features
            # In production, you'd need exact feature matching with training data
            
            # Calculate risk based on attendance decline and average attendance
            avg_attendance = student_data.get('Average_Attendance', 75)
            decline_score = student_data.get('Attendance_Decline_Score', 0)
            test_score = student_data.get('test_score', 75)
            
            # Simple risk calculation for demo
            risk_score = 0.0
            if avg_attendance < 60:
                risk_score += 0.4
            elif avg_attendance < 75:
                risk_score += 0.2
            
            if decline_score > 10:
                risk_score += 0.3
            elif decline_score > 5:
                risk_score += 0.1
            
            if test_score < 50:
                risk_score += 0.2
            elif test_score < 70:
                risk_score += 0.1
            
            # Cap at 1.0
            risk_score = min(risk_score, 1.0)
            
            # Determine prediction and risk level
            prediction = 1 if risk_score >= 0.7 else 0  # Updated: High risk threshold at 0.7
            
            if risk_score >= 0.7:
                risk_level = "High"
            elif risk_score >= 0.3:
                risk_level = "Medium"
            else:
                risk_level = "Low"
            
            return {
                "prediction": prediction,
                "risk_score": float(risk_score),
                "risk_level": risk_level,
                "student_id": student_data.get('student_id', 'Unknown'),
                "student_name": student_data.get('student_name', 'Student'),
                "student_email": student_data.get('student_email', '')
            }
            
        except Exception as e:
            raise Exception(f"Prediction error: {str(e)}")

predictor = AttendanceRiskPredictor()

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Attendance Risk Prediction API",
        "status": "running",
        "email_service": EMAIL_SERVICE_AVAILABLE,
        "endpoints": {
            "/predict": "POST - Predict attendance risk for a student",
            "/predict-batch": "POST - Predict attendance risk for multiple students",
            "/send-email": "POST - Send risk notification email to a student",
            "/send-batch-emails": "POST - Send risk notification emails to multiple students",
            "/health": "GET - Health check"
        }
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "models_loaded": decision_tree_model is not None and logistic_model is not None
    })

@app.route('/predict', methods=['POST'])
def predict_attendance_risk():
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['student_id', 'Average_Attendance']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Make prediction
        result = predictor.predict_risk(data, model_type="decision_tree")
        
        return jsonify({
            "success": True,
            "result": result
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict-batch', methods=['POST'])
def predict_batch():
    try:
        data = request.json
        
        if not data or 'students' not in data:
            return jsonify({"error": "No student data provided"}), 400
        
        students = data['students']
        total_students = len(students)
        
        # Process in smaller batches to avoid timeout
        batch_size = 100  # Process 100 students at a time
        results = []
        
        for i in range(0, total_students, batch_size):
            batch = students[i:i + batch_size]
            
            for student in batch:
                try:
                    result = predictor.predict_risk(student, model_type="decision_tree")
                    results.append(result)
                except Exception as e:
                    results.append({
                        "student_id": student.get('student_id', 'Unknown'),
                        "error": str(e)
                    })
            
            # Optional: Add a small delay between batches to prevent overwhelming
            if i + batch_size < total_students:
                import time
                time.sleep(0.1)  # 100ms delay between batches
        
        return jsonify({
            "success": True,
            "results": results,
            "total_processed": len(results)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/send-email', methods=['POST'])
def send_risk_email():
    """Send risk notification email to a single student"""
    if not EMAIL_SERVICE_AVAILABLE:
        return jsonify({"error": "Email service not available"}), 503
    
    try:
        data = request.json
        
        print(f"[EMAIL] Received email request for: {data.get('student_name', 'Unknown')}")
        print(f"[EMAIL] Email service type: {EMAIL_SERVICE_TYPE}")
        print(f"[EMAIL] Email service class: {type(email_service)}")
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['student_email', 'student_name', 'risk_level']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Only send emails for Medium and High risk
        if data['risk_level'] not in ['Medium', 'High']:
            return jsonify({
                "success": False,
                "message": f"No email sent - risk level is {data['risk_level']} (only Medium/High risk students receive emails)"
            })
        
        # Create email template and send
        print(f"[EMAIL] Creating email template...")
        subject, html_content, text_content = email_service.create_risk_email_template(data, data['risk_level'])
        print(f"[EMAIL] Sending email to: {data['student_email']}")
        result = email_service.send_email(
            data['student_email'], 
            subject, 
            html_content, 
            text_content
        )
        
        print(f"[EMAIL] Email result: {result}")
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/send-batch-emails', methods=['POST'])
def send_batch_risk_emails():
    """Send risk notification emails to multiple students"""
    if not EMAIL_SERVICE_AVAILABLE:
        return jsonify({"error": "Email service not available"}), 503
    
    try:
        data = request.json
        
        if not data or 'students' not in data:
            return jsonify({"error": "No student data provided"}), 400
        
        # Send batch emails
        results = email_service.send_batch_emails(data['students'])
        
        return jsonify({
            "success": True,
            "summary": {
                "total_processed": results['total_processed'],
                "emails_sent": results['sent_count'],
                "emails_failed": results['failed_count']
            },
            "details": results['results']
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/email-config', methods=['GET'])
def get_email_config():
    """Get email service configuration status"""
    return jsonify({
        "email_service_available": EMAIL_SERVICE_AVAILABLE,
        "email_service_type": EMAIL_SERVICE_TYPE,
        "api_provider": "Gmail SMTP" if EMAIL_SERVICE_AVAILABLE else None,
        "from_email": email_service.from_email if EMAIL_SERVICE_AVAILABLE else None,
        "api_key_configured": bool(email_service.api_key) if EMAIL_SERVICE_AVAILABLE else False,
        "instructions": {
            "setup": "Use Gmail with an App Password",
            "free_tier": "Free — uses Python built-in smtplib, no third-party service",
            "env_variable": "Set GMAIL_USER and GMAIL_APP_PASSWORD in .env",
            "example": "GMAIL_USER=you@gmail.com, GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx"
        }
    })

if __name__ == '__main__':
    print("[START] Starting Attendance Risk Prediction API...")
    print("[INFO] Models loaded:", decision_tree_model is not None and logistic_model is not None)
    print("[INFO] Server will be available at: http://localhost:5000")
    print("[INFO] API documentation: http://localhost:5000")
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)