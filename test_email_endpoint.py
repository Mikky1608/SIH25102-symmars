"""
Test the email endpoint directly
"""
import requests
import json

# Test data
test_student = {
    "student_name": "Test Student",
    "student_id": "TEST001",
    "student_email": "test@example.com",
    "risk_score": 0.85,
    "risk_level": "High",
    "Average_Attendance": 55.5,
    "Attendance_Decline_Score": 12.3
}

print("🧪 Testing Email Endpoint...")
print(f"Sending test email for: {test_student['student_name']}")

try:
    response = requests.post(
        "http://localhost:5000/send-email",
        json=test_student,
        timeout=10
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("\n✅ Email endpoint is working!")
        print("📧 Check your inbox: mithimikky15@gmail.com")
    else:
        print("\n❌ Email endpoint returned an error")
        
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
