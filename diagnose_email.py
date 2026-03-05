import smtplib
import ssl
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def diagnostic():
    print("--- Email Service Diagnostic ---")
    user = os.getenv('GMAIL_USER')
    password = os.getenv('GMAIL_APP_PASSWORD')
    
    print(f"GMAIL_USER set: {'Yes' if user else 'No'}")
    print(f"GMAIL_APP_PASSWORD set: {'Yes' if password else 'No'}")
    
    if not user or not password:
        print("\n[CRITICAL] Credentials missing! You must set GMAIL_USER and GMAIL_APP_PASSWORD in your deployment dashboard.")
        return

    hosts = [("smtp.gmail.com", 465), ("smtp.gmail.com", 587)]
    
    for host, port in hosts:
        print(f"\nTesting connection to {host}:{port}...")
        try:
            if port == 465:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(host, port, context=context, timeout=10) as server:
                    print(f"✅ Connection successful to port {port}")
            else:
                with smtplib.SMTP(host, port, timeout=10) as server:
                    server.starttls()
                    print(f"✅ Connection successful to port {port}")
        except Exception as e:
            print(f"❌ Connection failed to port {port}: {e}")

if __name__ == "__main__":
    diagnostic()
