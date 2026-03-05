# 📧 API-Based Email Notification System - Setup Guide

## 🎯 Overview

This advanced email notification system uses professional email API services instead of SMTP, providing:

- **Higher deliverability rates** (99%+ delivery success)
- **Better spam protection** (emails won't go to spam)
- **Professional email tracking** and analytics
- **Scalable infrastructure** for thousands of emails
- **University email addresses** for all students
- **Admin notifications** for at-risk students

## 🏫 Email Format

### **Student Emails:**
```
Format: firstname.lastname.studentid@university.edu
Examples:
- john.doe.101@university.edu
- jane.smith.102@university.edu
- amit.kumar.103@university.edu
```

### **Admin Email:**
```
admin@university.edu
```

## 🚀 Supported Email Providers

### **1. SendGrid (Recommended)**
- **Free Tier**: 100 emails/day
- **Paid Plans**: From $19.95/month (40,000 emails)
- **Best For**: High volume, excellent deliverability

### **2. Mailgun**
- **Free Tier**: 5,000 emails/month
- **Paid Plans**: Pay-as-you-go ($0.80/1000 emails)
- **Best For**: Developers, flexible pricing

### **3. Resend**
- **Free Tier**: 3,000 emails/month
- **Paid Plans**: From $20/month
- **Best For**: Modern API, great documentation

### **4. Brevo (Sendinblue)**
- **Free Tier**: 300 emails/day
- **Paid Plans**: From $25/month
- **Best For**: Marketing + transactional emails

## 📋 Setup Instructions

### **Step 1: Choose Your Email Provider**

Pick one of the providers above based on your needs. For this guide, we'll use **SendGrid** as an example.

### **Step 2: Sign Up and Get API Key**

#### **SendGrid Setup:**

1. Go to [SendGrid.com](https://sendgrid.com)
2. Sign up for a free account
3. Verify your email address
4. Go to **Settings** → **API Keys**
5. Click **Create API Key**
6. Name it: "Student Dropout System"
7. Select **Full Access** permissions
8. Copy the API key (you'll only see it once!)

#### **Mailgun Setup:**

1. Go to [Mailgun.com](https://mailgun.com)
2. Sign up for free account
3. Verify your domain or use sandbox domain
4. Go to **Settings** → **API Keys**
5. Copy your **Private API Key**

#### **Resend Setup:**

1. Go to [Resend.com](https://resend.com)
2. Sign up with GitHub or email
3. Go to **API Keys** section
4. Create new API key
5. Copy the key

#### **Brevo Setup:**

1. Go to [Brevo.com](https://brevo.com)
2. Sign up for free account
3. Go to **SMTP & API** → **API Keys**
4. Create new API key
5. Copy the key

### **Step 3: Configure Environment Variables**

Create a `.env` file in your project root:

```bash
# Email Provider Configuration
EMAIL_PROVIDER=sendgrid  # Options: sendgrid, mailgun, resend, brevo

# SendGrid Configuration
SENDGRID_API_KEY=your_sendgrid_api_key_here

# Mailgun Configuration (if using Mailgun)
MAILGUN_API_KEY=your_mailgun_api_key_here
MAILGUN_DOMAIN=mg.university.edu

# Resend Configuration (if using Resend)
RESEND_API_KEY=your_resend_api_key_here

# Brevo Configuration (if using Brevo)
BREVO_API_KEY=your_brevo_api_key_here

# University Configuration
ADMIN_EMAIL=admin@university.edu
UNIVERSITY_DOMAIN=university.edu
```

### **Step 4: Install Required Packages**

```bash
pip install requests python-dotenv
```

### **Step 5: Add University Emails to Datasets**

Run the script to add university emails to all student datasets:

```bash
python ml/code/add_university_emails.py
```

This will:
- Add `university_email` column to all datasets
- Generate emails in format: firstname.lastname.studentid@university.edu
- Update comprehensive, sample, and batch datasets

### **Step 6: Test the Email System**

Create a test script `test_api_email.py`:

```python
import os
from dotenv import load_dotenv
from notifications.api_email_service import APIEmailService

# Load environment variables
load_dotenv()

# Initialize email service
email_service = APIEmailService(provider='sendgrid')

# Test student data
test_student = {
    'student_name': 'John Doe',
    'student_id': '101',
    'student_email': 'john.doe.101@university.edu',
    'risk_score': 0.85,
    'Average_Attendance': 45.5,
    'Attendance_Decline_Score': 25.3
}

# Send test email
result = email_service.send_student_notification(test_student)

if result['success']:
    print("✅ Test email sent successfully!")
else:
    print(f"❌ Failed to send email: {result.get('error')}")
```

Run the test:
```bash
python test_api_email.py
```

## 🔧 Integration with Backend

Update your `backend/app.py` to use the API email service:

```python
# Add at the top of backend/app.py
from notifications.api_email_service import api_email_service

# Update the send-batch-emails endpoint
@app.route('/send-batch-emails', methods=['POST'])
def send_batch_emails():
    try:
        data = request.json
        students = data.get('students', [])
        
        # Send emails using API service
        results = api_email_service.send_batch_notifications(students)
        
        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

## 📊 Email Features

### **Student Notification Email Includes:**

1. **Professional HTML Design**
   - University branding
   - Color-coded by risk level (Red for High, Yellow for Medium)
   - Responsive layout for mobile devices

2. **Detailed Metrics**
   - Student ID
   - Risk Score (percentage)
   - Average Attendance
   - Attendance Decline Score
   - Risk Level Classification

3. **Actionable Recommendations**
   - Personalized based on risk level
   - Clear next steps
   - Contact information

4. **Call-to-Action Button**
   - Direct link to contact support
   - Easy access to help resources

### **Admin Notification Email Includes:**

1. **Student Alert Summary**
   - Student name and ID
   - Risk level and score
   - Contact information

2. **Action Required Notice**
   - Follow-up timeline (24-48 hours)
   - Intervention recommendations

## 🎯 Usage Examples

### **Send Single Student Notification:**

```python
from notifications.api_email_service import api_email_service

student_data = {
    'student_name': 'Jane Smith',
    'student_id': '102',
    'student_email': 'jane.smith.102@university.edu',
    'risk_score': 0.75,
    'Average_Attendance': 55.0,
    'Attendance_Decline_Score': 18.5
}

result = api_email_service.send_student_notification(student_data)
print(result)
```

### **Send Batch Notifications:**

```python
import pandas as pd
from notifications.api_email_service import api_email_service

# Load students from CSV
df = pd.read_csv('sample_batch_students.csv')

# Filter at-risk students (risk_score >= 0.3)
at_risk = df[df['risk_score'] >= 0.3]

# Convert to list of dictionaries
students_list = at_risk.to_dict('records')

# Send batch emails
results = api_email_service.send_batch_notifications(students_list)

print(f"Sent: {results['sent']}")
print(f"Failed: {results['failed']}")
print(f"Skipped: {results['skipped']}")
```

### **Generate University Email:**

```python
from notifications.api_email_service import api_email_service

email = api_email_service.generate_university_email('Amit Kumar', '103')
print(email)  # Output: amit.kumar.103@university.edu
```

## 📈 Monitoring & Analytics

### **Email Delivery Tracking:**

Most providers offer dashboards to track:
- Delivery rates
- Open rates
- Click rates
- Bounce rates
- Spam reports

### **Access Provider Dashboards:**

- **SendGrid**: https://app.sendgrid.com/statistics
- **Mailgun**: https://app.mailgun.com/app/analytics
- **Resend**: https://resend.com/emails
- **Brevo**: https://app.brevo.com/statistics

## 🔒 Security Best Practices

1. **Never commit API keys to Git**
   - Use `.env` file (add to `.gitignore`)
   - Use environment variables in production

2. **Rotate API keys regularly**
   - Change keys every 3-6 months
   - Immediately rotate if compromised

3. **Use least privilege access**
   - Only grant necessary permissions
   - Separate keys for dev/staging/production

4. **Monitor usage**
   - Set up alerts for unusual activity
   - Track email volume and patterns

## 🚨 Troubleshooting

### **Problem: Emails not sending**

**Solution:**
1. Check API key is correct
2. Verify provider is set correctly in `.env`
3. Check API quota/limits
4. Review provider dashboard for errors

### **Problem: Emails going to spam**

**Solution:**
1. Verify sender domain (use custom domain)
2. Set up SPF, DKIM, DMARC records
3. Warm up your sending domain gradually
4. Avoid spam trigger words

### **Problem: Rate limit errors**

**Solution:**
1. Check your plan limits
2. Implement rate limiting in code
3. Upgrade to higher tier plan
4. Use batch sending with delays

## 💰 Cost Comparison

| Provider | Free Tier | Cost per 10K emails | Best For |
|----------|-----------|---------------------|----------|
| **SendGrid** | 100/day | $1.00 | High volume |
| **Mailgun** | 5K/month | $0.80 | Pay-as-you-go |
| **Resend** | 3K/month | $0.67 | Modern API |
| **Brevo** | 300/day | $2.50 | Marketing |

## 🎓 Production Deployment

### **For 4,000 Students:**

**Recommended Setup:**
- **Provider**: SendGrid or Mailgun
- **Plan**: Paid tier (for reliability)
- **Estimated Cost**: $20-40/month
- **Email Volume**: ~400-800 emails/month (10-20% at-risk)

### **Scaling Considerations:**

- **10,000 students**: $50-80/month
- **50,000 students**: $200-300/month
- **100,000+ students**: Enterprise plans

## ✅ Checklist

Before going live:

- [ ] Sign up for email provider
- [ ] Get API key
- [ ] Configure `.env` file
- [ ] Add university emails to datasets
- [ ] Test with sample student
- [ ] Verify admin notifications work
- [ ] Check email deliverability
- [ ] Set up monitoring/alerts
- [ ] Document for team
- [ ] Train staff on system

## 🎉 Benefits Over SMTP

| Feature | API Service | SMTP |
|---------|-------------|------|
| **Deliverability** | 99%+ | 70-80% |
| **Spam Protection** | Excellent | Poor |
| **Scalability** | Unlimited | Limited |
| **Analytics** | Built-in | None |
| **Setup Complexity** | Easy | Complex |
| **Maintenance** | Low | High |
| **Cost** | Predictable | Variable |

## 📞 Support

### **Provider Support:**
- **SendGrid**: https://support.sendgrid.com
- **Mailgun**: https://help.mailgun.com
- **Resend**: https://resend.com/docs
- **Brevo**: https://help.brevo.com

### **System Support:**
- Check logs in `notifications/` directory
- Review API responses for errors
- Contact your email provider support

---

**🚀 Your professional email notification system is ready for Smart India Hackathon 2025!**

With university email addresses and API-based delivery, you have a production-ready system that can scale to thousands of students with excellent deliverability and professional presentation.
