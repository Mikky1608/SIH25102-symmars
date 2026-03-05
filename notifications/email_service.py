"""
Email Service - Gmail SMTP (Free & Open Source)
Uses Python's built-in smtplib + email.mime — no third-party API needed.
"""

import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

# Load environment variables from project root
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailService:
    """
    Free email service using Gmail SMTP via Python's built-in smtplib.
    Requires a Gmail App Password (not your regular Gmail password).
    """

    def __init__(self):
        self.gmail_user = os.getenv('GMAIL_USER', '')
        self.gmail_password = os.getenv('GMAIL_APP_PASSWORD', '')
        self.from_name = os.getenv('FROM_NAME', 'Student Success Center')
        self.admin_email = os.getenv('ADMIN_EMAIL', self.gmail_user)
        self.smtp_host = 'smtp.gmail.com'
        self.smtp_port = 465  # SSL (primary)
        self.smtp_alt_port = 587  # STARTTLS (fallback)

        # Demo mode — redirect all emails to one address for testing
        self.demo_mode = os.getenv('DEMO_MODE', 'false').lower() == 'true'
        self.demo_email = os.getenv('DEMO_EMAIL', '')

        # Expose api_key for compatibility with backend/app.py checks
        self.api_key = self.gmail_password
        self.from_email = self.gmail_user

        if not self.gmail_user or not self.gmail_password:
            logger.warning("[WARN] GMAIL_USER or GMAIL_APP_PASSWORD not set in .env")
        else:
            logger.info("[OK] Gmail SMTP email service ready")
            if self.demo_mode:
                logger.info(f"[DEMO] All emails will be redirected to: {self.demo_email}")

    def send_email(self, to_email: str, subject: str, html_content: str, text_content: str = "") -> Dict:
        """Send an email via Gmail SMTP using SSL."""

        if not self.gmail_user or not self.gmail_password:
            return {"success": False, "message": "Gmail credentials not configured in .env"}

        # Demo mode: redirect to test address
        original_email = to_email
        if self.demo_mode and self.demo_email:
            to_email = self.demo_email
            logger.info(f"[DEMO] Redirecting {original_email} -> {to_email}")

        try:
            # Build the MIME message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.gmail_user}>"
            msg['To'] = to_email

            # Attach plain text and HTML parts
            if text_content:
                msg.attach(MIMEText(text_content, 'plain'))
            msg.attach(MIMEText(html_content, 'html'))

            # Try Port 465 (SSL) first
            try:
                logger.info(f"[SMTP] Trying {self.smtp_host}:{self.smtp_port} (SSL)...")
                with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, timeout=5) as server:
                    server.login(self.gmail_user, self.gmail_password)
                    server.sendmail(self.gmail_user, to_email, msg.as_string())
                logger.info(f"[OK] Email sent successfully to {to_email} via port 465")
            except (smtplib.SMTPException, ConnectionError, TimeoutError, OSError) as e:
                logger.warning(f"[WARN] Port 465 failed: {e}. Trying port 587 (STARTTLS)...")
                
                # Fallback to Port 587 (STARTTLS)
                with smtplib.SMTP(self.smtp_host, self.smtp_alt_port, timeout=5) as server:
                    server.starttls()
                    server.login(self.gmail_user, self.gmail_password)
                    server.sendmail(self.gmail_user, to_email, msg.as_string())
                logger.info(f"[OK] Email sent successfully to {to_email} via port 587")

            return {
                "success": True,
                "message": "Email sent successfully via Gmail SMTP",
                "recipient": to_email,
                "original_recipient": original_email
            }

        except smtplib.SMTPAuthenticationError:
            msg = "Gmail authentication failed. Check GMAIL_USER and GMAIL_APP_PASSWORD in .env"
            logger.error(f"[ERROR] {msg}")
            return {"success": False, "message": msg}
        except smtplib.SMTPException as e:
            logger.error(f"[ERROR] SMTP error: {e}")
            return {"success": False, "message": f"SMTP error: {str(e)}"}
        except Exception as e:
            logger.error(f"[ERROR] Unexpected error: {type(e).__name__}: {e}")
            return {"success": False, "message": str(e)}

    def create_risk_email_template(self, student_data: Dict, risk_level: str) -> tuple:
        """Create email template — returns (subject, html, text)."""
        name = student_data.get('student_name', 'Student')
        student_id = student_data.get('student_id', 'N/A')
        risk_score = student_data.get('risk_score', 0) * 100
        attendance = student_data.get('Average_Attendance', 0)
        decline = student_data.get('Attendance_Decline_Score', 0)

        color = "#dc3545" if risk_level == "High" else "#ffc107"
        priority = "HIGH PRIORITY" if risk_level == "High" else "MEDIUM PRIORITY"

        subject = f"Academic Alert: {name} - {priority}"

        html = f"""<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f4f4f4;">
  <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
    <div style="background: {color}; color: white; padding: 30px; text-align: center;">
      <h1 style="margin: 0; font-size: 24px;">Student Success Center</h1>
      <p style="margin: 10px 0 0 0; font-size: 16px; font-weight: bold;">{priority}</p>
    </div>
    <div style="padding: 30px;">
      <h2 style="color: #333;">Dear {name},</h2>
      <p style="color: #555;">Our AI-powered system has identified attendance patterns that require your immediate attention.</p>

      <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid {color};">
        <h3 style="color: {color}; margin-top: 0;">Your Academic Metrics</h3>
        <table style="width: 100%; border-collapse: collapse;">
          <tr style="border-bottom: 1px solid #eee;"><td style="padding: 8px 0;"><strong>Student ID:</strong></td><td style="padding: 8px 0;">{student_id}</td></tr>
          <tr style="border-bottom: 1px solid #eee;"><td style="padding: 8px 0;"><strong>Risk Score:</strong></td><td style="padding: 8px 0; color: {color}; font-weight: bold;">{risk_score:.1f}%</td></tr>
          <tr style="border-bottom: 1px solid #eee;"><td style="padding: 8px 0;"><strong>Attendance:</strong></td><td style="padding: 8px 0;">{attendance:.1f}%</td></tr>
          <tr style="border-bottom: 1px solid #eee;"><td style="padding: 8px 0;"><strong>Decline Score:</strong></td><td style="padding: 8px 0;">{decline:.1f}</td></tr>
          <tr><td style="padding: 8px 0;"><strong>Risk Level:</strong></td><td style="padding: 8px 0; color: {color}; font-weight: bold;">{risk_level.upper()}</td></tr>
        </table>
      </div>

      <div style="background: #e8f4f8; border-left: 4px solid #17a2b8; padding: 20px; margin: 20px 0;">
        <h3 style="color: #17a2b8; margin-top: 0;">Recommended Actions</h3>
        <ul style="color: #555; margin: 0; padding-left: 20px;">
          <li>Schedule a meeting with your academic advisor</li>
          <li>Contact the Student Success Center</li>
          <li>Review your attendance patterns</li>
          <li>Access academic support services</li>
        </ul>
      </div>

      <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 20px; margin: 20px 0;">
        <h3 style="color: #856404; margin-top: 0;">Need Help?</h3>
        <p style="margin: 0; color: #555;">
          <strong>Student Success Center</strong><br>
          Email: {self.admin_email}<br>
          Office Hours: Mon-Fri, 9 AM - 5 PM
        </p>
      </div>

      <div style="text-align: center; margin: 30px 0;">
        <a href="mailto:{self.admin_email}"
           style="display: inline-block; background: {color}; color: white; padding: 15px 40px;
                  text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px;">
          Contact Support
        </a>
      </div>
    </div>
    <div style="background: #f8f9fa; padding: 20px; text-align: center; border-top: 1px solid #dee2e6;">
      <p style="color: #999; font-size: 12px; margin: 0;">
        &copy; 2026 Student Success Center &mdash; AI-Powered Dropout Prediction System<br>
        Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
      </p>
    </div>
  </div>
</body>
</html>"""

        text = f"""ACADEMIC ALERT — {priority}

Dear {name},

Our AI system has flagged your academic metrics for attention.

METRICS:
  Student ID   : {student_id}
  Risk Score   : {risk_score:.1f}%
  Attendance   : {attendance:.1f}%
  Decline Score: {decline:.1f}
  Risk Level   : {risk_level.upper()}

RECOMMENDED ACTIONS:
  - Schedule a meeting with your academic advisor
  - Contact the Student Success Center
  - Review your attendance patterns

CONTACT:
  Email : {self.admin_email}
  Hours : Mon-Fri, 9 AM - 5 PM

© 2026 Student Success Center
"""
        return subject, html, text

    def send_batch_emails(self, students_data: List[Dict]) -> Dict:
        """Send emails to multiple students in parallel using a thread pool."""
        total_processed = len(students_data)
        results = []
        
        # Prepare valid students (Medium/High risk only)
        at_risk_students = [s for s in students_data if s.get('risk_level', 'Low') in ['Medium', 'High']]
        skipped_count = total_processed - len(at_risk_students)
        
        for student in students_data:
            if student.get('risk_level', 'Low') not in ['Medium', 'High']:
                results.append({
                    'student_name': student.get('student_name'),
                    'status': 'skipped',
                    'message': 'Low risk — no email needed',
                    'success': True
                })

        def process_student(student):
            subject, html, text = self.create_risk_email_template(student, student.get('risk_level'))
            result = self.send_email(
                student.get('student_email', ''),
                subject,
                html,
                text
            )
            return {
                'student_name': student.get('student_name'),
                'student_email': student.get('student_email'),
                'risk_level': student.get('risk_level'),
                'status': 'sent' if result['success'] else 'failed',
                'success': result['success'],
                'message': result.get('message', '')
            }

        # Send in parallel (limit to 5 threads to avoid Gmail rate limiting)
        if at_risk_students:
            logger.info(f"[BATCH] Sending {len(at_risk_students)} emails in parallel...")
            with ThreadPoolExecutor(max_workers=5) as executor:
                parallel_results = list(executor.map(process_student, at_risk_students))
                results.extend(parallel_results)

        sent_count = sum(1 for r in results if r.get('status') == 'sent')
        failed_count = sum(1 for r in results if r.get('status') == 'failed')

        return {
            'total_processed': total_processed,
            'sent_count': sent_count,
            'failed_count': failed_count,
            'results': results
        }


# Singleton instance
email_service = EmailService()
