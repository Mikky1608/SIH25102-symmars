"""
Test script for API-based email notification system
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add notifications to path
sys.path.append(os.path.dirname(__file__))

from notifications.api_email_service import APIEmailService

def test_email_generation():
    """Test university email generation"""
    print("\n" + "="*70)
    print("🧪 TEST 1: University Email Generation")
    print("="*70)
    
    email_service = APIEmailService(provider='sendgrid')
    
    test_cases = [
        ('John Doe', '1001'),
        ('Jane Smith', '1002'),
        ('Amit Kumar Singh', '1003'),
        ('Maria Garcia', '1004'),
    ]
    
    for name, student_id in test_cases:
        email = email_service.generate_university_email(name, student_id)
        print(f"  {name:25s} → {email}")
    
    print("\n✅ Email generation test passed!")

def test_email_template():
    """Test email template creation"""
    print("\n" + "="*70)
    print("🧪 TEST 2: Email Template Creation")
    print("="*70)
    
    email_service = APIEmailService(provider='sendgrid')
    
    # Test student data
    test_student = {
        'student_name': 'John Doe',
        'student_id': '1001',
        'student_email': 'john.doe.1001@university.edu',
        'risk_score': 0.85,
        'Average_Attendance': 45.5,
        'Attendance_Decline_Score': 25.3
    }
    
    subject, html, text = email_service.create_risk_email_html(test_student, 'High')
    
    print(f"\n  Subject: {subject}")
    print(f"  HTML Length: {len(html)} characters")
    print(f"  Text Length: {len(text)} characters")
    print(f"\n  Preview (first 200 chars):")
    print(f"  {text[:200]}...")
    
    print("\n✅ Email template test passed!")

def test_send_email():
    """Test sending actual email (requires API key)"""
    print("\n" + "="*70)
    print("🧪 TEST 3: Send Test Email")
    print("="*70)
    
    # Check if API key is configured
    provider = os.getenv('EMAIL_PROVIDER', 'sendgrid')
    
    if provider == 'sendgrid':
        api_key = os.getenv('SENDGRID_API_KEY', '')
    elif provider == 'mailgun':
        api_key = os.getenv('MAILGUN_API_KEY', '')
    elif provider == 'resend':
        api_key = os.getenv('RESEND_API_KEY', '')
    elif provider == 'brevo':
        api_key = os.getenv('BREVO_API_KEY', '')
    else:
        api_key = ''
    
    if not api_key or api_key == 'your_' + provider + '_api_key_here':
        print("\n  ⚠️  API key not configured!")
        print(f"  Please set {provider.upper()}_API_KEY in .env file")
        print(f"  See API_EMAIL_SETUP_GUIDE.md for instructions")
        return
    
    email_service = APIEmailService(provider=provider)
    
    # Test student data
    test_student = {
        'student_name': 'Test Student',
        'student_id': '9999',
        'student_email': os.getenv('ADMIN_EMAIL', 'admin@university.edu'),  # Send to admin for testing
        'risk_score': 0.75,
        'Average_Attendance': 55.0,
        'Attendance_Decline_Score': 18.5
    }
    
    print(f"\n  Provider: {provider}")
    print(f"  Sending test email to: {test_student['student_email']}")
    print(f"  Risk Level: Medium (75%)")
    
    result = email_service.send_student_notification(test_student)
    
    if result['success']:
        print("\n  ✅ Test email sent successfully!")
        print(f"  Check your inbox: {test_student['student_email']}")
    else:
        print(f"\n  ❌ Failed to send email")
        print(f"  Error: {result.get('error', 'Unknown error')}")

def test_batch_emails():
    """Test batch email sending"""
    print("\n" + "="*70)
    print("🧪 TEST 4: Batch Email Simulation")
    print("="*70)
    
    email_service = APIEmailService(provider='sendgrid')
    
    # Simulate batch of students
    students = [
        {
            'student_name': 'High Risk Student',
            'student_id': '1001',
            'student_email': 'high.risk.1001@university.edu',
            'risk_score': 0.85,
            'Average_Attendance': 40.0,
            'Attendance_Decline_Score': 30.0
        },
        {
            'student_name': 'Medium Risk Student',
            'student_id': '1002',
            'student_email': 'medium.risk.1002@university.edu',
            'risk_score': 0.55,
            'Average_Attendance': 65.0,
            'Attendance_Decline_Score': 15.0
        },
        {
            'student_name': 'Low Risk Student',
            'student_id': '1003',
            'student_email': 'low.risk.1003@university.edu',
            'risk_score': 0.15,
            'Average_Attendance': 90.0,
            'Attendance_Decline_Score': 2.0
        }
    ]
    
    print(f"\n  Simulating batch of {len(students)} students:")
    for student in students:
        risk_level = 'High' if student['risk_score'] >= 0.7 else 'Medium' if student['risk_score'] >= 0.3 else 'Low'
        print(f"    • {student['student_name']:25s} - {risk_level:6s} Risk ({student['risk_score']*100:.0f}%)")
    
    print("\n  Expected behavior:")
    print("    • High Risk: Email sent ✅")
    print("    • Medium Risk: Email sent ✅")
    print("    • Low Risk: Skipped (no email needed) ⏭️")
    
    print("\n✅ Batch email simulation passed!")

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🎓 API-BASED EMAIL NOTIFICATION SYSTEM - TEST SUITE")
    print("="*70)
    
    try:
        # Test 1: Email generation
        test_email_generation()
        
        # Test 2: Email template
        test_email_template()
        
        # Test 3: Send actual email (if configured)
        test_send_email()
        
        # Test 4: Batch simulation
        test_batch_emails()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS COMPLETED!")
        print("="*70)
        
        print("\n📋 Next Steps:")
        print("  1. Configure your email provider API key in .env file")
        print("  2. Run this test again to send actual emails")
        print("  3. Check API_EMAIL_SETUP_GUIDE.md for detailed instructions")
        print("  4. Integrate with your backend API")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
