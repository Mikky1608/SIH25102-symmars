@echo off
echo Starting Backend Server with Email Configuration...
set RESEND_API_KEY=%RESEND_API_KEY%
set FROM_EMAIL=onboarding@resend.dev
set FROM_NAME=Student Success Center
set ADMIN_EMAIL=admin@university.edu
python backend/app.py
