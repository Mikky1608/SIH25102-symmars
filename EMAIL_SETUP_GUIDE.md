# 📧 Email Notification Setup Guide

## 🎯 Overview
The Student Dropout Prediction System includes an automated email notification feature that sends personalized alerts to students at Medium and High risk of dropping out.

## 📋 Prerequisites
- Gmail account for sending emails
- Gmail App Password (not your regular password)
- Environment variables configured

## 🔧 Step-by-Step Setup

### Step 1: Enable Gmail App Password

1. **Go to your Google Account**
   - Visit: https://myaccount.google.com/
   - Sign in to your Gmail account

2. **Enable 2-Factor Authentication**
   - Go to Security → 2-Step Verification
   - Follow the setup process if not already enabled

3. **Generate App Password**
   - Go to Security → App passwords
   - Select "Mail" and "Windows Computer" (or appropriate options)
   - Click "Generate"
   - **Copy the 16-character password** (you'll need this)

### Step 2: Set Environment Variables

#### **Option A: Windows (Command Prompt)**
```cmd
set SENDER_EMAIL=your-email@gmail.com
set SENDER_PASSWORD=your-16-character-app-password
```

#### **Option B: Windows (PowerShell)**
```powershell
$env:SENDER_EMAIL="your-email@gmail.com"
$env:SENDER_PASSWORD="your-16-character-app-password"
```

#### **Option C: Create .env file**
Create a file named `.env` in the project root:
```
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-16-character-app-password
```

### Step 3: Restart the Backend Server

After setting environment variables:
1. Stop the current backend server (Ctrl+C)
2. Restart it: `python backend/app.py`
3. Check the logs for "Email service available"

### Step 4: Test Email Functionality

1. Go to the web dashboard: http://localhost:8501
2. Navigate to "Batch Prediction"
3. Upload a CSV file with student data
4. Run predictions
5. Look for the "📧 Email Notifications" section
6. Click "Send Email Notifications" to test

## 📧 Email Features

### **Automatic Email Triggers**
- **Medium Risk Students**: Receive proactive support emails
- **High Risk Students**: Receive urgent intervention emails
- **Low Risk Students**: No emails sent (to avoid spam)

### **Email Content**
- **Personalized**: Uses student name and specific data
- **Risk-Specific**: Different templates for Medium vs High risk
- **Professional**: HTML formatted with institutional branding
- **Actionable**: Includes specific recommendations and contact info

### **Email Templates**

#### **High Risk Email**
- 🚨 Subject: "Urgent: Academic Support Needed"
- Red color scheme indicating urgency
- Immediate action recommendations
- Emergency contact information

#### **Medium Risk Email**
- 📊 Subject: "Academic Performance Alert"
- Yellow color scheme for caution
- Proactive support recommendations
- Regular support contact information

## 🔍 Troubleshooting

### **Common Issues**

#### **"Email service not available"**
- Check environment variables are set correctly
- Restart the backend server
- Verify Gmail App Password is correct

#### **"Authentication failed"**
- Ensure 2-Factor Authentication is enabled
- Use App Password, not regular Gmail password
- Check for typos in email/password

#### **"Connection timeout"**
- Check internet connection
- Verify Gmail SMTP is not blocked by firewall
- Try different network if corporate firewall blocks SMTP

#### **"Invalid email address"**
- Ensure CSV file has `student_email` column
- Check email format is valid (contains @)
- Verify email addresses are not empty

### **Testing Email Setup**

#### **Test 1: Check Configuration**
```bash
curl http://localhost:5000/email-config
```
Should return: `"email_service_available": true`

#### **Test 2: Send Single Email**
```bash
curl -X POST http://localhost:5000/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "student_email": "test@gmail.com",
    "student_name": "Test Student",
    "risk_level": "High",
    "risk_score": 0.85,
    "Average_Attendance": 45.5,
    "Attendance_Decline_Score": 25.3
  }'
```

## 📊 Email Analytics

### **Batch Email Results**
After sending batch emails, you'll see:
- **Total Processed**: Number of Medium/High risk students
- **Emails Sent**: Successfully delivered emails
- **Failed**: Emails that couldn't be sent
- **Detailed Log**: Individual results for each student

### **Success Metrics**
- Email delivery confirmation
- Student engagement tracking (if implemented)
- Response rates to support services

## 🔒 Security & Privacy

### **Data Protection**
- Emails contain only necessary academic information
- No sensitive personal data included
- Professional, supportive tone maintained

### **Email Security**
- Uses Gmail's secure SMTP with TLS encryption
- App passwords are more secure than regular passwords
- Environment variables keep credentials safe

### **Compliance**
- Follows educational communication best practices
- Includes opt-out information if required
- Maintains professional institutional standards

## 🎯 Best Practices

### **Email Frequency**
- Send notifications weekly or bi-weekly
- Avoid daily emails to prevent spam perception
- Coordinate with academic calendar

### **Content Guidelines**
- Keep messages supportive, not punitive
- Focus on available resources and help
- Include clear next steps for students

### **Monitoring**
- Track email delivery rates
- Monitor student response to interventions
- Adjust messaging based on effectiveness

## 📞 Support

### **If You Need Help**
1. Check the troubleshooting section above
2. Verify all setup steps were completed
3. Test with a simple email first
4. Check backend server logs for error messages

### **Email Template Customization**
The email templates can be customized in:
- `notifications/email_service.py`
- Look for the `create_risk_email_template` function
- Modify HTML content, colors, and messaging as needed

---

**🎓 Ready to help students succeed with automated, caring communication!**