import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_email():
    load_dotenv()
    user = os.getenv('GMAIL_USER')
    password = os.getenv('GMAIL_APP_PASSWORD')
    to = os.getenv('ADMIN_EMAIL', user)
    
    print(f"Testing Gmail SMTP for user: {user}")
    print(f"Attempting to send test email to: {to}")
    
    if not user or not password:
        print("Error: GMAIL_USER or GMAIL_APP_PASSWORD not found in .env")
        return

    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = to
    msg['Subject'] = "SMTP Connectivity Test"
    msg.attach(MIMEText("This is a test email to verify SMTP configuration.", 'plain'))
    
    try:
        print("Connecting to smtp.gmail.com:465...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            print("Logging in...")
            server.login(user, password)
            print("Sending email...")
            server.sendmail(user, to, msg.as_string())
        print("Success! Email sent.")
    except Exception as e:
        print(f"Failure: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_email()
