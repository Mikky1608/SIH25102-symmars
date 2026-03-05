# 📧 Resend Email Service Setup Guide

## 🎯 Why Resend?

**Resend** is a modern, developer-friendly email API that's perfect for educational projects and hackathons:

✅ **Free Tier**: 3,000 emails/month, 100 emails/day  
✅ **No Credit Card Required** for free tier  
✅ **Open-Source Friendly**: Simple REST API  
✅ **Professional**: Used by companies worldwide  
✅ **Easy Setup**: Get started in 5 minutes  

## 🚀 Quick Setup (5 Minutes)

### **Step 1: Create Free Resend Account**

1. Go to [https://resend.com/signup](https://resend.com/signup)
2. Sign up with your email (no credit card needed)
3. Verify your email address
4. You're in! 🎉

### **Step 2: Get Your API Key**

1. Log in to [https://resend.com/api-keys](https://resend.com/api-keys)
2. Click **"Create API Key"**
3. Name it: `Student Dropout Prediction System`
4. Copy the API key (starts with `re_...`)
5. **Important**: Save it securely - you won't see it again!

### **Step 3: Configure Your Project**

#### **Option A: Using Environment Variables (Recommended)**

**Windows (PowerShell):**
```powershell
$env:RESEND_API_KEY="re_your_api_key_here"
$env:FROM_EMAIL="onboarding@resend.dev"
$env:FROM_NAME="Student Success Center"
$env:ADMIN_EMAIL="your-email@example.com"
```

**Windows (CMD):**
```cmd
set RESEND_API_KEY=re_your_api_key_here
set FROM_EMAIL=onboarding@resend.dev
set FROM_NAME=Student Success Center
set ADMIN_EMAIL=your-email@example.com
```

**Linux/Mac:**
```bash
export RESEND_API_KEY="re_your_api_key_here"
export FROM_EMAIL="onboarding@resend.dev"
export FROM_NAME="Student Success Center"
export ADMIN_EMAIL="your-email@example.com"
```

#### **Option B: Using .env File**

Create a `.env` file in your project root:

```env
# Resend Email Configuration
RESEND_API_KEY=re_your_api_key_here
FROM_EMAIL=onboarding@resend.dev
FROM_NAME=Student Success Center
ADMIN_EMAIL=your-email@example.com
```

### **Step 4: Test Your Setup**

Run the test script:

```bash
python test_resend_email.py
```

You should see:
```
✅ Resend email service initialized successfully
📧 Sending from: Student Success Center <onboarding@resend.dev>
✅ Email sent successfully to test@example.com
```

## 📧 Email Configuration Options

### **FROM_EMAIL Options:**

#### **1. Resend Test Email (Default - Works Immediately)**
```env
FROM_EMAIL=onboarding@resend.dev
```
- ✅ Works immediately, no setup needed
- ✅ Perfect for testing and demos
- ⚠️ Shows "via resend.dev" in email clients

#### **2. Your Own Domain (Professional)**
```env
FROM_EMAIL=noreply@youruniversity.edu
```
- ✅ Professional appearance
- ✅ Better deliverability
- ⚠️ Requires domain verification (takes 5-10 minutes)

**To use your own domain:**
1. Go to [https://resend.com/domains](https://resend.com/domains)
2. Click "Add Domain"
3. Enter your domain (e.g., `youruniversity.edu`)
4. Add the DNS records shown (ask your IT department)
5. Wait for verification (usually 5-10 minutes)
6. Update `FROM_EMAIL` to use your domain

## 🎯 Usage in Your Project

### **Backend Integration**

The email service is already integrated in `backend/app.py`:

```python
# Email endpoints available:
POST /send-email          # Send single email
POST /send-batch-emails   # Send multiple emails
GET  /email-config        # Check email service status
```

### **Frontend Integration**

The Streamlit dashboard already has email functionality:

1. Go to **Batch Prediction** tab
2. Upload CSV file with student data
3. Click **"Predict All Students"**
4. Click **"📧 Send Email Notifications"**
5. View delivery report

## 📊 Free Tier Limits

| Feature | Free Tier | Notes |
|---------|-----------|-------|
| **Emails/Month** | 3,000 | Perfect for hackathons |
| **Emails/Day** | 100 | Enough for demos |
| **API Calls** | Unlimited | No restrictions |
| **Support** | Community | Active Discord community |
| **Cost** | $0 | No credit card required |

## 🔧 Troubleshooting

### **Issue: "RESEND_API_KEY not configured"**

**Solution:**
```bash
# Check if environment variable is set
echo $RESEND_API_KEY  # Linux/Mac
echo %RESEND_API_KEY%  # Windows CMD
$env:RESEND_API_KEY    # Windows PowerShell

# If empty, set it:
export RESEND_API_KEY="re_your_key_here"  # Linux/Mac
set RESEND_API_KEY=re_your_key_here       # Windows CMD
$env:RESEND_API_KEY="re_your_key_here"    # Windows PowerShell
```

### **Issue: "Failed to send email: Invalid API key"**

**Solution:**
1. Check your API key is correct (starts with `re_`)
2. Make sure there are no extra spaces
3. Regenerate API key if needed at [https://resend.com/api-keys](https://resend.com/api-keys)

### **Issue: Emails not arriving**

**Solution:**
1. Check spam/junk folder
2. Verify recipient email is correct
3. Check Resend dashboard for delivery status: [https://resend.com/emails](https://resend.com/emails)
4. Make sure you haven't exceeded daily limit (100 emails/day)

### **Issue: "Rate limit exceeded"**

**Solution:**
- Free tier: 100 emails/day
- Wait 24 hours or upgrade to paid plan
- For hackathons, 100/day is usually sufficient

## 🎓 For Hackathon Judges

### **Demo-Ready Features:**

1. **Professional Email Templates**
   - HTML emails with university branding
   - Risk-based color coding (Red for High, Yellow for Medium)
   - Personalized student data

2. **Automated Notifications**
   - AI-powered risk detection
   - Automatic email sending to at-risk students
   - Batch processing for multiple students

3. **Real-Time Tracking**
   - Delivery status monitoring
   - Success/failure reporting
   - Email analytics

### **Live Demo Steps:**

1. Upload sample CSV: `sample_batch_students.csv`
2. Run predictions (shows 99.875% accuracy)
3. Send email notifications (shows real-time progress)
4. View delivery report (shows sent/failed/skipped)
5. Check actual email in inbox (professional HTML template)

## 📚 Additional Resources

- **Resend Documentation**: [https://resend.com/docs](https://resend.com/docs)
- **API Reference**: [https://resend.com/docs/api-reference](https://resend.com/docs/api-reference)
- **Community Support**: [https://resend.com/discord](https://resend.com/discord)
- **Status Page**: [https://status.resend.com](https://status.resend.com)

## 🎉 You're All Set!

Your Student Dropout Prediction System now has a professional, production-ready email notification system powered by Resend!

**Next Steps:**
1. Test with sample data
2. Customize email templates (optional)
3. Add your university branding (optional)
4. Demo to hackathon judges! 🏆

---

**Need Help?**
- Check the [Resend Documentation](https://resend.com/docs)
- Join the [Resend Discord](https://resend.com/discord)
- Review `test_resend_email.py` for examples
