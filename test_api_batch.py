import requests
import json

data = {
    "students": [
        {
            "student_id": 1001,
            "student_name": "Test User",
            "student_email": "mithimikky15@gmail.com",
            "Average_Attendance": 50.0,
            "Attendance_Decline_Score": 12.0
        }
    ]
}

print("Sending batch prediction request...")
response = requests.post("http://127.0.0.1:5000/predict-batch", json=data)

print(f"Status: {response.status_code}")
try:
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Failed to parse JSON: {e}")
    print(response.text)
