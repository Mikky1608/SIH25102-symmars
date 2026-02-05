@echo off
echo ====================================
echo Email Service Setup for Student Dropout Prediction System
echo ====================================
echo.

echo Please enter your Gmail credentials for sending notifications:
echo.

set /p SENDER_EMAIL="Enter your Gmail address: "
set /p SENDER_PASSWORD="Enter your Gmail App Password (16 characters): "

echo.
echo Setting environment variables...

setx SENDER_EMAIL "%SENDER_EMAIL%"
setx SENDER_PASSWORD "%SENDER_PASSWORD%"

echo.
echo ====================================
echo Environment variables set successfully!
echo ====================================
echo.
echo SENDER_EMAIL: %SENDER_EMAIL%
echo SENDER_PASSWORD: [HIDDEN]
echo.
echo IMPORTANT: 
echo 1. Restart your command prompt/terminal
echo 2. Restart the backend server: python backend/app.py
echo 3. Test email functionality in the web dashboard
echo.
echo For detailed setup instructions, see EMAIL_SETUP_GUIDE.md
echo.
pause