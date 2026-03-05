"""
Test script for Resend email service
Run this to verify your email configuration is working
"""

import os
import sys
sys.path.append('notifications')

from resend_email_service import ResendEmailService

def test_email_service():
    """Test the Resend email service"""
    print("="*70)
    print("🧪 TESTING RESEND EMAIL SERVICE")
    print("="*70)
    
    # Initialize service
    email_service = ResendEmailService()
    
    # Check configuration
    print("\n📋 Configuration Check:")
    print(f"  API Key Set: {'✅ Yes' if email_service.api_key else '❌ No'}")
    print(f"  From Email: {email_service.from_email}")
    print(f"  From Name: {email_service.from_name}")
    print(f"  Admin Email: {email_service.admin_email}")
    
    if not email_service.api_key:
        print("\n❌ ERROR: RESEND_API_KEY not set!")
        print("\n📝 Setup Instructions:")
        print("  1. Get your free API key at: https://resend.com/signup")
        print("  2. Set environment variable:")
        print("     Windows (PowerShell): $env:RESEND_API_KEY='re_your_key_here'")
        print("     Windows (CMD): set RESEND_API_KEY=re_your_key_here")
        print("     Linux/Mac: export RESEND_API_KEY='re_your_key_here'")
        return False
    
    # Test email data
    test_student = {
        'student_name': 'John Doe',
        'student_id': 'TEST001',
        'student_email': input("\n📧 Enter your email to receive test notification: ").strip(),
        'risk_score': 0.85,
        'Average_Attendance': 55.5,
        'Attendance_Decline_Score': 12.3,
        'risk_level': 'High'
    }
    
    print("\n📤 Sending test email...")
    print(f"  To: {test_student['student_email']}")
    print(f"  Risk Level: {test_student['risk_level']}")
    
    # Create email template
    subject, html_content, text_content = email_service.create_risk_email_template(
        test_student,
        test_student['risk_level']
    )
    
    print(f"  Subject: {subject}")
    
    # Send email
    result = email_service.send_email(
        test_student['student_email'],
        subject,
        html_content,
        text_content
    )
    
    print("\n" + "="*70)
    if result['success']:
        print("✅ TEST PASSED!")
        print(f"📧 Email sent successfully to {test_student['student_email']}")
        print(f"📝 Email ID: {result.get('email_id', 'N/A')}")
        print("\n💡 Check your inbox (and spam folder) for the test email!")
    else:
        print("❌ TEST FAILED!")
        print(f"Error: {result.get('message', 'Unknown error')}")
        print("\n🔧 Troubleshooting:")
        print("  1. Verify your API key is correct")
        print("  2. Check your internet connection")
        print("  3. Visit https://resend.com/emails to see delivery status")
    print("="*70)
    
    return result['success']

def test_batch_emails():
    """Test batch email sending"""
    print("\n" + "="*70)
    print("🧪 TESTING BATCH EMAIL SENDING")
    print("="*70)
    
    email_service = ResendEmailService()
    
    if not email_service.api_key:
        print("❌ RESEND_API_KEY not set. Skipping batch test.")
        return False
    
    test_email = input("\n📧 Enter your email for batch test (or press Enter to skip): ").strip()
    
    if not test_email:
        print("⏭️  Skipping batch test")
        return True
    
    # Test batch data
    test_students = [
        {
            'student_name': 'Alice Johnson',
            'student_id': 'TEST002',
            'student_email': test_email,
            'risk_score': 0.75,
            'Average_Attendance': 62.0,
            'Attendance_Decline_Score': 8.5,
            'risk_level': 'High'
        },
        {
            'student_name': 'Bob Smith',
            'student_id': 'TEST003',
            'student_email': test_email,
            'risk_score': 0.45,
            'Average_Attendance': 68.0,
            'Attendance_Decline_Score': 4.2,
            'risk_level': 'Medium'
        },
        {
            'student_name': 'Charlie Brown',
            'student_id': 'TEST004',
            'student_email': test_email,
            'risk_score': 0.15,
            'Average_Attendance': 88.0,
            'Attendance_Decline_Score': 1.0,
            'risk_level': 'Low'
        }
    ]
    
    print(f"\n📤 Sending batch emails to {len(test_students)} students...")
    
    results = email_service.send_batch_emails(test_students)
    
    print("\n📊 Batch Results:")
    print(f"  Total: {results['total']}")
    print(f"  ✅ Sent: {results['sent']}")
    print(f"  ❌ Failed: {results['failed']}")
    print(f"  ⏭️  Skipped: {results['skipped']} (Low risk students)")
    
    print("\n📋 Details:")
    for detail in results['details']:
        status_icon = "✅" if detail['status'] == 'sent' else "⏭️" if detail['status'] == 'skipped' else "❌"
        print(f"  {status_icon} {detail['student_name']} ({detail['student_id']}): {detail['message']}")
    
    print("="*70)
    return results['sent'] > 0

if __name__ == "__main__":
    print("\n🎓 Student Dropout Prediction System")
    print("📧 Resend Email Service Test\n")
    
    # Test single email
    single_test_passed = test_email_service()
    
    if single_test_passed:
        # Test batch emails
        batch_test_passed = test_batch_emails()
        
        if batch_test_passed:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ Your email system is ready for production!")
        else:
            print("\n⚠️  Single email test passed, batch test skipped or failed")
    else:
        print("\n❌ Email service not configured properly")
        print("📝 Please follow the setup guide in RESEND_EMAIL_SETUP.md")
    
    print("\n" + "="*70)
