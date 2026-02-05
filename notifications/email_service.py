import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        # Email configuration - using Gmail SMTP
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv('SENDER_EMAIL', 'your-email@gmail.com')
        self.sender_password = os.getenv('SENDER_PASSWORD', 'your-app-password')
        self.sender_name = "Student Success Center"
        
    def create_risk_email_template(self, student_data, risk_level):
        """Create personalized email template based on risk level"""
        
        student_name = student_data.get('student_name', 'Student')
        student_id = student_data.get('student_id', 'N/A')
        risk_score = student_data.get('risk_score', 0)
        avg_attendance = student_data.get('Average_Attendance', 0)
        decline_score = student_data.get('Attendance_Decline_Score', 0)
        
        # Email templates based on risk level
        if risk_level == "High":
            subject = f"🚨 Urgent: Academic Support Needed - {student_name}"
            color = "#dc3545"  # Red
            priority = "HIGH PRIORITY"
            message_tone = "immediate attention"
            recommendations = [
                "Schedule an immediate meeting with your academic advisor",
                "Contact the Student Success Center within 24 hours",
                "Review your current course load and attendance patterns",
                "Consider academic support services and tutoring programs",
                "Speak with your instructors about makeup opportunities"
            ]
        else:  # Medium risk
            subject = f"📊 Academic Performance Alert - {student_name}"
            color = "#ffc107"  # Yellow
            priority = "MEDIUM PRIORITY"
            message_tone = "proactive support"
            recommendations = [
                "Schedule a meeting with your academic advisor this week",
                "Review your attendance and study habits",
                "Consider joining study groups or tutoring sessions",
                "Reach out to instructors if you're struggling with coursework",
                "Utilize campus resources for academic support"
            ]
        
        # Create HTML email template
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{subject}</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center;">
                <h1 style="margin: 0; font-size: 24px;">🎓 Student Success Center</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">Academic Performance Monitoring System</p>
            </div>
            
            <div style="background: white; padding: 30px; border: 1px solid #ddd; border-top: none;">
                
                <div style="background: {color}; color: white; padding: 15px; border-radius: 5px; margin-bottom: 25px; text-align: center;">
                    <h2 style="margin: 0; font-size: 18px;">{priority}</h2>
                    <p style="margin: 5px 0 0 0;">This message requires {message_tone}</p>
                </div>
                
                <h2 style="color: #333; margin-bottom: 20px;">Dear {student_name},</h2>
                
                <p>We hope this message finds you well. Our academic monitoring system has identified some patterns in your academic performance that we'd like to discuss with you.</p>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #495057; margin-top: 0;">📊 Your Current Academic Status</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; border-bottom: 1px solid #dee2e6;"><strong>Student ID:</strong></td>
                            <td style="padding: 8px 0; border-bottom: 1px solid #dee2e6;">{student_id}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; border-bottom: 1px solid #dee2e6;"><strong>Risk Level:</strong></td>
                            <td style="padding: 8px 0; border-bottom: 1px solid #dee2e6; color: {color}; font-weight: bold;">{risk_level}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; border-bottom: 1px solid #dee2e6;"><strong>Risk Score:</strong></td>
                            <td style="padding: 8px 0; border-bottom: 1px solid #dee2e6;">{risk_score:.2f}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; border-bottom: 1px solid #dee2e6;"><strong>Average Attendance:</strong></td>
                            <td style="padding: 8px 0; border-bottom: 1px solid #dee2e6;">{avg_attendance:.1f}%</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0;"><strong>Attendance Trend:</strong></td>
                            <td style="padding: 8px 0;">{"Declining" if decline_score > 5 else "Stable"}</td>
                        </tr>
                    </table>
                </div>
                
                <h3 style="color: #495057;">🎯 Recommended Actions</h3>
                <ul style="padding-left: 20px;">
        """
        
        for recommendation in recommendations:
            html_template += f"<li style='margin-bottom: 8px;'>{recommendation}</li>"
        
        html_template += f"""
                </ul>
                
                <div style="background: #e3f2fd; padding: 20px; border-radius: 5px; margin: 25px 0; border-left: 4px solid #2196f3;">
                    <h4 style="color: #1976d2; margin-top: 0;">💡 Remember</h4>
                    <p style="margin-bottom: 0;">Academic challenges are temporary, and we're here to support you every step of the way. Early intervention is key to academic success, and taking action now can make a significant difference in your educational journey.</p>
                </div>
                
                <h3 style="color: #495057;">📞 Get Help Now</h3>
                <div style="background: #f1f8e9; padding: 15px; border-radius: 5px; margin: 15px 0;">
                    <p style="margin: 0;"><strong>📧 Email:</strong> success@institute.edu</p>
                    <p style="margin: 5px 0;"><strong>📱 Phone:</strong> (555) 123-4567</p>
                    <p style="margin: 5px 0;"><strong>🏢 Office:</strong> Student Success Center, Room 201</p>
                    <p style="margin: 5px 0 0 0;"><strong>🕒 Hours:</strong> Monday-Friday, 9:00 AM - 5:00 PM</p>
                </div>
                
                <p style="margin-top: 25px;">We believe in your potential and are committed to helping you succeed. Please don't hesitate to reach out if you have any questions or concerns.</p>
                
                <p>Best regards,<br>
                <strong>Student Success Team</strong><br>
                Academic Support Services</p>
                
            </div>
            
            <div style="background: #6c757d; color: white; padding: 20px; border-radius: 0 0 10px 10px; text-align: center; font-size: 12px;">
                <p style="margin: 0;">This is an automated message from the Student Success Center</p>
                <p style="margin: 5px 0 0 0;">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            
        </body>
        </html>
        """
        
        return subject, html_template
    
    def send_email(self, recipient_email, subject, html_content, student_name="Student"):
        """Send email to recipient"""
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.sender_name} <{self.sender_email}>"
            message["To"] = recipient_email
            
            # Create HTML part
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Create secure connection and send email
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            logger.info(f"Email sent successfully to {recipient_email} ({student_name})")
            return {"success": True, "message": f"Email sent to {student_name}"}
            
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
            return {"success": False, "message": f"Failed to send email: {str(e)}"}
    
    def send_batch_emails(self, students_data):
        """Send emails to multiple students based on their risk levels"""
        results = []
        sent_count = 0
        failed_count = 0
        
        for student in students_data:
            risk_level = student.get('risk_level', 'Low')
            
            # Only send emails for Medium and High risk students
            if risk_level in ['Medium', 'High']:
                student_email = student.get('student_email', '')
                student_name = student.get('student_name', 'Student')
                
                if student_email and '@' in student_email:
                    # Create personalized email
                    subject, html_content = self.create_risk_email_template(student, risk_level)
                    
                    # Send email
                    result = self.send_email(student_email, subject, html_content, student_name)
                    result['student_name'] = student_name
                    result['student_email'] = student_email
                    result['risk_level'] = risk_level
                    results.append(result)
                    
                    if result['success']:
                        sent_count += 1
                    else:
                        failed_count += 1
                else:
                    results.append({
                        'success': False,
                        'message': 'Invalid email address',
                        'student_name': student_name,
                        'student_email': student_email,
                        'risk_level': risk_level
                    })
                    failed_count += 1
        
        return {
            'total_processed': len([s for s in students_data if s.get('risk_level') in ['Medium', 'High']]),
            'sent_count': sent_count,
            'failed_count': failed_count,
            'results': results
        }

# Create global email service instance
email_service = EmailService()