# 🎓 Student Dropout Prediction System - Workflow Block Diagram

## 📊 Complete System Architecture & Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           🎯 STUDENT DROPOUT PREDICTION SYSTEM                          │
│                              Smart India Hackathon 2025                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    📊 DATA LAYER                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    │
│  │   📚 Students   │  │  👨‍👩‍👧‍👦 Parents   │  │   👨‍🏫 Mentors   │  │  📈 Attendance  │    │
│  │   Institute1    │  │   Institute1    │  │   Institute1    │  │   Institute1    │    │
│  │   Institute2    │  │   Institute2    │  │   Institute2    │  │   Institute2    │    │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘    │
│           │                     │                     │                     │           │
│           └─────────────────────┼─────────────────────┼─────────────────────┘           │
│                                 │                     │                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                        │
│  │  📊 Test Scores │  │ 📧 Email Dataset│  │ 🎯 Sample Data  │                        │
│  │   Institute1    │  │  4000+ Students │  │  100 Students   │                        │
│  │   Institute2    │  │ Gmail Addresses │  │  10 Batch Test  │                        │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              🔧 DATA PROCESSING LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                           📊 Feature Engineering                                │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │   │
│  │  │  Attendance %   │  │ Score Averages  │  │ Decline Trends  │                │   │
│  │  │  Weekly Trends  │  │ Performance     │  │ Risk Indicators │                │   │
│  │  │  Missing Days   │  │ Ratios          │  │ Parent Factors  │                │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘                │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                         │                                               │
│                                         ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                        🧹 Data Preprocessing                                    │   │
│  │  • Label Encoding (Categorical → Numerical)                                    │   │
│  │  • Standard Scaling (Feature Normalization)                                    │   │
│  │  • Missing Value Handling                                                      │   │
│  │  • Correlation Analysis                                                        │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                               🤖 MACHINE LEARNING LAYER                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                            🎯 Model Training                                    │   │
│  │                                                                                 │   │
│  │  ┌─────────────────────┐              ┌─────────────────────┐                  │   │
│  │  │   🌳 Decision Tree   │              │ 📊 Logistic Regr.  │                  │   │
│  │  │                     │              │                     │                  │   │
│  │  │  Accuracy: 99.875%  │              │  Accuracy: 99.5%    │                  │   │
│  │  │  Max Depth: 10      │              │  C=1.0, Solver=lbfgs│                  │   │
│  │  │  Min Samples: 2     │              │  Max Iter: 1000     │                  │   │
│  │  │                     │              │                     │                  │   │
│  │  └─────────────────────┘              └─────────────────────┘                  │   │
│  │              │                                    │                            │   │
│  │              └────────────────┬───────────────────┘                            │   │
│  │                               │                                                │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐  │   │
│  │  │                    💾 Model Persistence                                │  │   │
│  │  │  • decision_tree_model.pkl                                             │  │   │
│  │  │  • logistic_model.pkl                                                  │  │   │
│  │  │  • scaler.pkl                                                          │  │   │
│  │  └─────────────────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                🌐 BACKEND API LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                          🔥 Flask REST API                                      │   │
│  │                         (Port: 5000)                                           │   │
│  │                                                                                 │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │   │
│  │  │ GET /health     │  │ POST /predict   │  │ POST /batch     │                │   │
│  │  │ System Status   │  │ Single Student  │  │ Multiple        │                │   │
│  │  │ Check           │  │ Risk Prediction │  │ Students CSV    │                │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘                │   │
│  │                                                                                 │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │   │
│  │  │ POST /send-email│  │ POST /batch-    │  │ GET /email-     │                │   │
│  │  │ Single Email    │  │ emails          │  │ config          │                │   │
│  │  │ Notification    │  │ Bulk Emails     │  │ Service Status  │                │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘                │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                         │                                               │
│                                         ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                        🎯 Risk Classification                                   │   │
│  │                                                                                 │   │
│  │  🔴 High Risk (≥ 70%):    Immediate intervention required                      │   │
│  │  🟡 Medium Risk (30-69%): Proactive monitoring needed                          │   │
│  │  🟢 Low Risk (< 30%):     Regular monitoring sufficient                        │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              📧 NOTIFICATION LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                         📧 Email Service System                                 │   │
│  │                                                                                 │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐   │   │
│  │  │                      🎨 HTML Email Templates                            │   │   │
│  │  │                                                                         │   │   │
│  │  │  ┌─────────────────┐              ┌─────────────────┐                  │   │   │
│  │  │  │ 🚨 High Risk    │              │ ⚠️  Medium Risk │                  │   │   │
│  │  │  │ Template        │              │ Template        │                  │   │   │
│  │  │  │                 │              │                 │                  │   │   │
│  │  │  │ • Red Theme     │              │ • Yellow Theme  │                  │   │   │
│  │  │  │ • Urgent Tone   │              │ • Supportive    │                  │   │   │
│  │  │  │ • Immediate     │              │ • Proactive     │                  │   │   │
│  │  │  │   Action        │              │   Guidance      │                  │   │   │
│  │  │  └─────────────────┘              └─────────────────┘                  │   │   │
│  │  └─────────────────────────────────────────────────────────────────────────┘   │   │
│  │                                         │                                       │   │
│  │                                         ▼                                       │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐   │   │
│  │  │                    📬 Gmail SMTP Integration                            │   │   │
│  │  │                                                                         │   │   │
│  │  │  • Server: smtp.gmail.com:587                                          │   │   │
│  │  │  • TLS Encryption                                                      │   │   │
│  │  │  • App Password Authentication                                         │   │   │
│  │  │  • Batch Processing Support                                            │   │   │
│  │  │  • Delivery Tracking                                                   │   │   │
│  │  └─────────────────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                               🖥️  FRONTEND LAYER                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                        🎨 Streamlit Dashboard                                   │   │
│  │                         (Port: 8501)                                           │   │
│  │                                                                                 │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐   │   │
│  │  │                        📊 Main Features                                 │   │   │
│  │  │                                                                         │   │   │
│  │  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │   │   │
│  │  │  │ 👤 Single       │  │ 📊 Batch        │  │ 📧 Email        │        │   │   │
│  │  │  │ Student         │  │ Prediction      │  │ Notifications   │        │   │   │
│  │  │  │ Prediction      │  │                 │  │                 │        │   │   │
│  │  │  │                 │  │ • CSV Upload    │  │ • Auto Send     │        │   │   │
│  │  │  │ • Manual Input  │  │ • Progress Bar  │  │ • Delivery      │        │   │   │
│  │  │  │ • Risk Gauge    │  │ • Results Table │  │   Tracking      │        │   │   │
│  │  │  │ • Recommendations│  │ • Statistics    │  │ • Status Report │        │   │   │
│  │  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │   │   │
│  │  └─────────────────────────────────────────────────────────────────────────┘   │   │
│  │                                         │                                       │   │
│  │                                         ▼                                       │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐   │   │
│  │  │                      📈 Interactive Visualizations                     │   │   │
│  │  │                                                                         │   │   │
│  │  │  • Risk Score Gauge Charts                                             │   │   │
│  │  │  • Attendance Trend Graphs                                             │   │   │
│  │  │  • Performance Distribution Charts                                     │   │   │
│  │  │  • Risk Level Pie Charts                                               │   │   │
│  │  │  • Correlation Heatmaps                                                │   │   │
│  │  └─────────────────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              👥 USER INTERACTION LAYER                                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                           🎯 User Workflows                                      │   │
│  │                                                                                 │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐   │   │
│  │  │                    📊 Single Student Analysis                           │   │   │
│  │  │                                                                         │   │   │
│  │  │  1. Enter student details manually                                     │   │   │
│  │  │  2. Click "Predict Risk"                                               │   │   │
│  │  │  3. View risk score & gauge visualization                              │   │   │
│  │  │  4. Get personalized recommendations                                   │   │   │
│  │  │  5. Optional: Send email notification                                  │   │   │
│  │  └─────────────────────────────────────────────────────────────────────────┘   │   │
│  │                                         │                                       │   │
│  │                                         ▼                                       │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐   │   │
│  │  │                     📈 Batch Processing Workflow                        │   │   │
│  │  │                                                                         │   │   │
│  │  │  1. Upload CSV file with student data                                  │   │   │
│  │  │  2. System validates and processes data                                │   │   │
│  │  │  3. ML models predict risk for all students                            │   │   │
│  │  │  4. View results table with risk classifications                       │   │   │
│  │  │  5. Download results or send email notifications                       │   │   │
│  │  │  6. View delivery reports and statistics                               │   │   │
│  │  └─────────────────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                               📊 OUTPUT & RESULTS LAYER                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                          🎯 Prediction Results                                  │   │
│  │                                                                                 │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │   │
│  │  │ 📊 Risk Score   │  │ 🏷️  Risk Level   │  │ 📈 Confidence   │                │   │
│  │  │                 │  │                 │  │                 │                │   │
│  │  │ 0.0 - 1.0       │  │ High/Med/Low    │  │ Model Accuracy  │                │   │
│  │  │ Probability     │  │ Classification  │  │ 99.875%         │                │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘                │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                         │                                               │
│                                         ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                        💡 Actionable Recommendations                            │   │
│  │                                                                                 │   │
│  │  🔴 High Risk Students:                                                         │   │
│  │    • Immediate counselor meeting                                                │   │
│  │    • Academic support services                                                 │   │
│  │    • Parent/guardian notification                                              │   │
│  │    • Weekly progress monitoring                                                │   │
│  │                                                                                 │   │
│  │  🟡 Medium Risk Students:                                                       │   │
│  │    • Proactive check-ins                                                       │   │
│  │    • Study group recommendations                                               │   │
│  │    • Attendance improvement plan                                               │   │
│  │    • Peer mentoring programs                                                   │   │
│  │                                                                                 │   │
│  │  🟢 Low Risk Students:                                                          │   │
│  │    • Continue current performance                                              │   │
│  │    • Regular monitoring                                                        │   │
│  │    • Leadership opportunities                                                  │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              🔄 SYSTEM INTEGRATION FLOW                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Frontend (Streamlit) ←→ Backend API (Flask) ←→ ML Models ←→ Email Service             │
│       │                        │                     │              │                  │
│       │                        │                     │              │                  │
│  User Interface          Risk Prediction        Model Inference   Notifications        │
│  Data Visualization      Batch Processing       Feature Scaling   SMTP Delivery        │
│  File Upload            API Endpoints           Classification    Template Rendering    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                🚀 DEPLOYMENT OPTIONS                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  🌐 Local Development:     python run_project.py                                       │
│  ☁️  Cloud Hosting:        Railway, Heroku, AWS, Google Cloud                          │
│  📱 Demo Deployment:       Streamlit Community Cloud                                   │
│  🐳 Containerization:      Docker support ready                                        │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## 🎯 Key System Metrics

| Component | Technology | Performance | Status |
|-----------|------------|-------------|---------|
| **ML Models** | Scikit-learn | 99.875% Accuracy | ✅ Ready |
| **Backend API** | Flask + CORS | 6 Endpoints | ✅ Ready |
| **Frontend** | Streamlit | Interactive Dashboard | ✅ Ready |
| **Email System** | Gmail SMTP | HTML Templates | ✅ Ready |
| **Data Processing** | Pandas + NumPy | 4000+ Records | ✅ Ready |
| **Risk Classification** | Custom Logic | 3-Tier System | ✅ Ready |

## 🔄 Data Flow Summary

1. **Data Input** → CSV files or manual entry
2. **Processing** → Feature engineering & scaling  
3. **Prediction** → ML models generate risk scores
4. **Classification** → Risk levels assigned (High/Medium/Low)
5. **Visualization** → Interactive charts and gauges
6. **Notification** → Automated emails to at-risk students
7. **Reporting** → Delivery tracking and analytics

## 🎓 Perfect for Smart India Hackathon 2025!

This comprehensive system demonstrates:
- **Advanced AI/ML** implementation
- **Full-stack development** capabilities  
- **Real-world problem solving** for education
- **Scalable architecture** design
- **Professional deployment** readiness