# SIH25102-symmars
Smart India Hackathon 2025 Project - AI-based drop-out prediction and counseling system

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# For Windows users
run_project.bat

# For Linux/Mac users
python run_project.py
```

### Option 2: Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start backend API (in one terminal)
python backend/app.py

# 3. Start frontend dashboard (in another terminal)
streamlit run frontend/app.py
```

### 🌐 Access Points
- **Frontend Dashboard**: http://localhost:8501
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/health

## 📊 Features
- **Single Student Prediction**: Analyze individual student risk
- **Batch Processing**: Upload CSV files for multiple students
- **Interactive Dashboard**: Real-time visualizations and insights
- **Risk Assessment**: AI-powered dropout prediction with 99.9% accuracy
- **Actionable Recommendations**: Specific intervention strategies
- **📧 Email Notifications**: Automated alerts to at-risk students


## 📂 Project Structure

<details>
<summary>Click to view</summary>
  
Data Engineer (Yashika/Mrinalendu/Ritik) → Works inside data/ (raw + processed).

Backend Dev (Shubhra/Manaswini) → Works inside backend/.

ML Engineer (Shubh) → Works inside ml/.

Frontend Dev (Shubhra/Manaswini) → Works inside frontend/.

Notification Engineer (Ritik/Yashika/Mrinalendu) → Works inside notifications/.

Presentation Lead (Mrinalendu/Ritik/Yashika) → Works inside docs/.
```bash
SIH25102-symmars/
├── backend/                     # APIs + risk scoring logic
│   ├── app.py                   # Main FastAPI/Flask app
│   ├── models/                  # DB models (if using SQLAlchemy)
│   ├── routes/                  # API endpoints
│   └── database.db              # SQLite (or migrations if Postgres)
│
├── data/                        # Raw + processed datasets
│   ├── raw/                     # Attendance, test scores, fees (CSVs)
│   └── processed/               # Cleaned/merged datasets
│
├── ml/                          # ML models and experiments
│   ├── notebooks/               # Jupyter notebooks for training
│   ├── models/                  # Saved models (pkl/joblib)
│   └── train.py                 # Training script
│
├── frontend/                    # Dashboard UI
│   ├── app.py                   # Streamlit entry point
│   ├── components/              # Custom charts, widgets
│   └── assets/                  # Images, CSS
│
├── notifications/               # Alerts and integration
│   ├── notifier.py              # Email/WhatsApp/SMS logic
│   └── templates/               # Message templates
│
├── docs/                        # Presentation + documentation
│   ├── architecture.png
│   ├── SIH-pitch-deck.pptx
│   └── readme-extras.md
│
├── .gitignore
├── requirements.txt             # Dependencies
├── README.md
