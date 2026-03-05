import smtplib
import ssl
from email.message import EmailMessage
import sys

sender = "mithimikky15@gmail.com"
password = "slqo neul eduz zpko"
receiver = "mithimikky15@gmail.com"

msg = EmailMessage()
msg.set_content("This is a detailed SMTP debug test.")
msg['Subject'] = "Smart India Hackathon - Debug Test"
msg['From'] = f"Student Success Center <{sender}>"
msg['To'] = receiver

print("Starting SMTP session with debug level 1...")
try:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.set_debuglevel(1)
        server.login(sender, password)
        server.send_message(msg)
    print("\nSUCCESS: SMTP transaction completed.")
except Exception as e:
    print(f"\nERROR: {e}")
