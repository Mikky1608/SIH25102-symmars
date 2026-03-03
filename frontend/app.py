import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import time

# Page configuration
st.set_page_config(
    page_title="Student Dropout Prediction System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .risk-high {
        color: #d62728;
        font-weight: bold;
    }
    .risk-medium {
        color: #ff7f0e;
        font-weight: bold;
    }
    .risk-low {
        color: #2ca02c;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Backend API URL
# Backend API URL handling
try:
    if "BACKEND_URL" in st.secrets:
        API_URL = st.secrets["BACKEND_URL"]
    else:
        import os
        API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5000")
except:
    import os
    API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5000")

# Ensure consistency
API_URL = API_URL.strip().rstrip('/')
if API_URL and not API_URL.startswith(('http://', 'https://')):
    API_URL = f"https://{API_URL}"

def check_api_health():
    """Check if the backend API is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            return True, "Healthy"
        return False, f"API returned status {response.status_code}"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"

def predict_risk(student_data):
    """Send prediction request to backend API"""
    try:
        response = requests.post(f"{API_URL}/predict", json=student_data, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"error": f"Connection Error: {str(e)}"}

def predict_batch(students_data):
    """Send batch prediction request to backend API"""
    try:
        response = requests.post(f"{API_URL}/predict-batch", json={"students": students_data}, timeout=120)  # Increased timeout to 2 minutes
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"error": f"Connection Error: {str(e)}"}

def send_batch_emails(students_data):
    """Send batch emails to at-risk students"""
    try:
        response = requests.post(f"{API_URL}/send-batch-emails", json={"students": students_data}, timeout=120)  # Increased timeout
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"error": f"Connection Error: {str(e)}"}

def check_email_service():
    """Check if email service is available"""
    try:
        response = requests.get(f"{API_URL}/email-config", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"email_service_available": False}
    except:
        return {"email_service_available": False}

def main():
    # Header
    st.markdown('<h1 class="main-header">🎓 Student Dropout Prediction System</h1>', unsafe_allow_html=True)
    st.markdown("**AI-powered early warning system for student attendance risk prediction**")
    
    # Check API status
    api_success, api_message = check_api_health()
    if api_success:
        st.success("✅ Backend API is running")
    else:
        st.error(f"❌ Backend API is not accessible: {api_message}")
        st.info(f"Current API URL: `{API_URL}`")
        st.markdown(f"""
        **Troubleshooting steps:**
        1. Ensure your **Railway backend** is running and shows "Success".
        2. Verify you added `BACKEND_URL` in **Streamlit Cloud Settings > Secrets**.
        3. Double-check the URL matches your Railway public domain.
        """)
        return
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "Single Student Prediction", 
        "Batch Prediction", 
        "Sample Data Analysis",
        "About System"
    ])
    
    if page == "Single Student Prediction":
        single_student_prediction()
    elif page == "Batch Prediction":
        batch_prediction()
    elif page == "Sample Data Analysis":
        sample_data_analysis()
    else:
        about_system()

def single_student_prediction():
    st.header("🔍 Single Student Risk Prediction")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Student Information")
        
        # Basic info
        student_id = st.number_input("Student ID", min_value=1, value=1001)
        student_name = st.text_input("Student Name", value="John Doe")
        institute_id = st.selectbox("Institute", [1, 2], index=0)
        
        # Academic info
        test_score = st.slider("Latest Test Score", 0, 100, 75)
        max_score = st.number_input("Maximum Score", min_value=1, value=100)
        
        # Attendance info
        st.subheader("Attendance Data")
        avg_attendance = st.slider("Average Attendance (%)", 0, 100, 75)
        decline_score = st.slider("Attendance Decline Score", 0, 50, 5)
        
        # Weekly attendance (simplified)
        st.subheader("Recent Weekly Attendance")
        week_attendance = []
        cols = st.columns(4)
        for i in range(12):
            with cols[i % 4]:
                week_val = st.number_input(f"Week {i+1}", 0, 100, max(0, avg_attendance - i*2), key=f"week_{i}")
                week_attendance.append(week_val)
    
    with col2:
        st.subheader("Prediction Results")
        
        if st.button("🎯 Predict Risk", type="primary"):
            # Prepare student data
            student_data = {
                "student_id": student_id,
                "student_name": student_name,
                "institute_id": institute_id,
                "test_score": test_score,
                "max_score": max_score,
                "avg_score_ratio": test_score / max_score,
                "Average_Attendance": avg_attendance,
                "Attendance_Decline_Score": decline_score,
            }
            
            # Add weekly attendance
            for i, attendance in enumerate(week_attendance):
                student_data[f"Week_{i+1}_Attendance"] = attendance
            
            # Make prediction
            with st.spinner("Analyzing student data..."):
                result = predict_risk(student_data)
            
            if "error" in result:
                st.error(f"Prediction failed: {result['error']}")
            else:
                prediction_result = result["result"]
                
                # Display results
                risk_level = prediction_result["risk_level"]
                risk_score = prediction_result["risk_score"]
                prediction = prediction_result["prediction"]
                
                # Risk level styling
                if risk_level == "High":
                    risk_color = "🔴"
                    risk_class = "risk-high"
                elif risk_level == "Medium":
                    risk_color = "🟡"
                    risk_class = "risk-medium"
                else:
                    risk_color = "🟢"
                    risk_class = "risk-low"
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{risk_color} Risk Level: <span class="{risk_class}">{risk_level}</span></h3>
                    <p><strong>Risk Score:</strong> {risk_score:.2f}</p>
                    <p><strong>Prediction:</strong> {'At Risk' if prediction == 1 else 'Not At Risk'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Risk gauge chart
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = risk_score * 100,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Risk Score (%)"},
                    delta = {'reference': 50},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 30], 'color': "lightgreen"},
                            {'range': [30, 70], 'color': "yellow"},
                            {'range': [70, 100], 'color': "red"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 70  # 70% = 0.7 threshold for High risk
                        }
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                # Recommendations
                st.subheader("📋 Recommendations")
                if risk_level == "High":
                    st.error("""
                    **Immediate Action Required:**
                    - Schedule urgent counseling session
                    - Contact parents/guardians
                    - Implement personalized support plan
                    - Monitor daily attendance
                    """)
                elif risk_level == "Medium":
                    st.warning("""
                    **Monitor Closely:**
                    - Weekly check-ins with mentor
                    - Track attendance trends
                    - Provide additional academic support
                    - Early intervention strategies
                    """)
                else:
                    st.success("""
                    **Continue Current Support:**
                    - Maintain regular monitoring
                    - Recognize good performance
                    - Continue engagement activities
                    """)

def batch_prediction():
    st.header("📊 Batch Student Risk Prediction")
    
    # File upload
    uploaded_file = st.file_uploader("Upload CSV file with student data", type=['csv'])
    
    # Initialize session state for batch results
    if 'batch_results' not in st.session_state:
        st.session_state.batch_results = None
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Loaded {len(df)} students")
            
            # Show processing time warning for large datasets
            if len(df) > 1000:
                st.warning(f"⚠️ Large dataset detected ({len(df)} students). Processing may take 2-3 minutes.")
            elif len(df) > 500:
                st.info(f"📊 Medium dataset ({len(df)} students). Processing may take 1-2 minutes.")
            else:
                st.info(f"📊 Dataset size: {len(df)} students. Processing should complete quickly.")
            
            # Show data preview
            st.subheader("Data Preview")
            st.dataframe(df.head())
            
            if st.button("🎯 Predict All Students", type="primary"):
                # Convert DataFrame to list of dictionaries
                students_data = df.to_dict('records')
                
                # Show progress information
                st.info(f"🔄 Processing {len(students_data)} students... This may take a few moments for large datasets.")
                
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                with st.spinner("Analyzing all students..."):
                    # Update progress
                    progress_bar.progress(25)
                    status_text.text("Sending data to prediction engine...")
                    
                    result = predict_batch(students_data)
                    
                    progress_bar.progress(75)
                    status_text.text("Processing results...")
                
                # Complete progress
                progress_bar.progress(100)
                status_text.text("Analysis complete!")
                
                if "error" in result:
                    st.error(f"Batch prediction failed: {result['error']}")
                    st.session_state.batch_results = None
                else:
                    # Store results in session state to persist between reruns
                    st.session_state.batch_results = result["results"]
            
            # If we have results in session state, display them
            if st.session_state.batch_results is not None:
                results = st.session_state.batch_results
                
                # Create results DataFrame
                results_df = pd.DataFrame(results)
                    
                # Display summary
                st.subheader("📈 Prediction Summary")
                
                col1, col2, col3, col4 = st.columns(4)
                
                total_students = len(results_df)
                high_risk = len(results_df[results_df['risk_level'] == 'High'])
                medium_risk = len(results_df[results_df['risk_level'] == 'Medium'])
                low_risk = len(results_df[results_df['risk_level'] == 'Low'])
                
                col1.metric("Total Students", total_students)
                col2.metric("High Risk", high_risk, delta=f"{high_risk/total_students*100:.1f}%")
                col3.metric("Medium Risk", medium_risk, delta=f"{medium_risk/total_students*100:.1f}%")
                col4.metric("Low Risk", low_risk, delta=f"{low_risk/total_students*100:.1f}%")
                    
                # Risk distribution chart
                risk_counts = results_df['risk_level'].value_counts()
                fig = px.pie(values=risk_counts.values, names=risk_counts.index, 
                           title="Risk Level Distribution",
                           color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'})
                st.plotly_chart(fig, use_container_width=True)
                
                # Detailed results
                st.subheader("📋 Detailed Results")
                
                # Filter options
                risk_filter = st.selectbox("Filter by Risk Level", ["All", "High", "Medium", "Low"])
                
                if risk_filter != "All":
                    filtered_df = results_df[results_df['risk_level'] == risk_filter]
                else:
                    filtered_df = results_df
                
                # Style the dataframe
                def style_risk_level(val):
                    if val == 'High':
                        return 'background-color: #ffcccc'
                    elif val == 'Medium':
                        return 'background-color: #fff2cc'
                    else:
                        return 'background-color: #ccffcc'
                
                styled_df = filtered_df.style.applymap(style_risk_level, subset=['risk_level'])
                st.dataframe(styled_df, use_container_width=True)
                
                # Download results
                csv = results_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name="student_risk_predictions.csv",
                    mime="text/csv"
                )
                
                # Email notification section
                st.subheader("📧 Email Notifications")
                
                # Check email service availability
                email_config = check_email_service()
                
                if email_config.get('email_service_available', False):
                    # Count students who would receive emails
                    at_risk_students = results_df[results_df['risk_level'].isin(['Medium', 'High'])]
                    
                    if len(at_risk_students) > 0:
                        st.info(f"📊 {len(at_risk_students)} students (Medium/High risk) are eligible for email notifications")
                        
                        # Show preview of students who will receive emails
                        with st.expander("👀 Preview Students Who Will Receive Emails"):
                            preview_cols = ['student_name', 'student_email', 'risk_level', 'risk_score']
                            available_cols = [col for col in preview_cols if col in at_risk_students.columns]
                            st.dataframe(at_risk_students[available_cols])
                        
                        # Email sending button
                        if st.button("📧 Send Email Notifications", type="secondary", help="Send personalized emails to Medium and High risk students"):
                            # Prepare student data for email
                            students_for_email = []
                            for _, row in at_risk_students.iterrows():
                                student_data = row.to_dict()
                                students_for_email.append(student_data)
                            
                            # Send emails
                            with st.spinner("Sending email notifications..."):
                                email_result = send_batch_emails(students_for_email)
                            
                            if "error" in email_result:
                                st.error(f"❌ Email sending failed: {email_result['error']}")
                            else:
                                summary = email_result.get('summary', {})
                                
                                # Show visual "Pop up" notifications
                                st.balloons()
                                st.toast("✅ All emails have been processed successfully!", icon='📧')
                                
                                st.success(f"✅ Email notifications sent successfully!")
                                
                                # Show email summary in a nice card
                                with st.container():
                                    col_a, col_b, col_c = st.columns(3)
                                    # Ensure summary is a dict for linting/runtime safety
                                    safe_summary = summary if isinstance(summary, dict) else {}
                                    col_a.metric("📧 Emails Sent", safe_summary.get('emails_sent', 0))
                                    col_b.metric("❌ Failed", safe_summary.get('emails_failed', 0))
                                    col_c.metric("📊 Processed", safe_summary.get('total_processed', 0))
                                
                                # Show detailed results
                                if st.checkbox("🔍 Show detailed email logs"):
                                    details = email_result.get('details', [])
                                    email_details_df = pd.DataFrame(details)
                                    if not email_details_df.empty:
                                        st.dataframe(email_details_df[['student_name', 'student_email', 'risk_level', 'success', 'message']], use_container_width=True)
                    else:
                        st.info("✅ No students require email notifications (all are Low risk)")
                    
                else:
                    st.warning("⚠️ Email service is not configured")
                    
                    with st.expander("📧 Email Setup Instructions"):
                        st.markdown("""
                        **To enable email notifications:**
                        
                        1. **Set up Gmail App Password:**
                           - Go to your Google Account settings
                           - Enable 2-Factor Authentication
                           - Generate an App Password for this application
                        
                        2. **Configure Environment Variables:**
                           ```bash
                           SENDER_EMAIL=your-email@gmail.com
                           SENDER_PASSWORD=your-app-password
                           ```
                        
                        3. **Restart the backend server**
                        
                        4. **Test the email functionality**
                        
                        **Note:** The system uses Gmail SMTP for sending emails.
                        """)
                    
                    # Show which students would receive emails if configured
                    at_risk_students = results_df[results_df['risk_level'].isin(['Medium', 'High'])]
                    if len(at_risk_students) > 0:
                        st.info(f"📊 {len(at_risk_students)} students would receive email notifications if email service was configured")
                        
                        with st.expander("👀 Students Who Would Receive Emails"):
                            preview_cols = ['student_name', 'student_email', 'risk_level', 'risk_score']
                            available_cols = [col for col in preview_cols if col in at_risk_students.columns]
                            if available_cols:
                                st.dataframe(at_risk_students[available_cols])
                            else:
                                st.dataframe(at_risk_students)
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    else:
        # Show sample format
        st.info("Please upload a CSV file with student data")
        st.subheader("📝 Required CSV Format")
        
        sample_data = {
            'student_id': [1001, 1002, 1003],
            'student_name': ['John Doe', 'Jane Smith', 'Bob Wilson'],
            'institute_id': [1, 1, 2],
            'test_score': [85, 45, 92],
            'Average_Attendance': [78.3, 32.5, 86.5],
            'Attendance_Decline_Score': [5.0, 15.0, 2.0]
        }
        
        sample_df = pd.DataFrame(sample_data)
        st.dataframe(sample_df)
        
        # Download sample
        csv = sample_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Sample CSV",
            data=csv,
            file_name="sample_student_data.csv",
            mime="text/csv"
        )

def sample_data_analysis():
    st.header("📊 Sample Data Analysis")
    
    # Create sample data for demonstration
    np.random.seed(42)
    n_students = 100
    
    sample_data = {
        'student_id': range(1001, 1001 + n_students),
        'student_name': [f'Student_{i}' for i in range(n_students)],
        'institute_id': np.random.choice([1, 2], n_students),
        'test_score': np.random.normal(75, 15, n_students).clip(0, 100),
        'Average_Attendance': np.random.normal(80, 20, n_students).clip(0, 100),
        'Attendance_Decline_Score': np.random.exponential(5, n_students).clip(0, 30)
    }
    
    df = pd.DataFrame(sample_data)
    
    # Generate predictions for sample data
    if st.button("🎯 Analyze Sample Data", type="primary"):
        students_data = df.to_dict('records')
        
        with st.spinner("Analyzing sample students..."):
            result = predict_batch(students_data)
        
        if "error" not in result:
            results_df = pd.DataFrame(result["results"])
            
            # Merge with original data
            analysis_df = df.merge(results_df[['student_id', 'risk_level', 'risk_score']], on='student_id')
            
            # Analysis charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Risk distribution
                fig1 = px.histogram(analysis_df, x='risk_level', 
                                  title="Risk Level Distribution",
                                  color='risk_level',
                                  color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'})
                st.plotly_chart(fig1, use_container_width=True)
                
                # Test score vs Risk
                fig3 = px.box(analysis_df, x='risk_level', y='test_score',
                            title="Test Scores by Risk Level",
                            color='risk_level',
                            color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'})
                st.plotly_chart(fig3, use_container_width=True)
            
            with col2:
                # Attendance vs Risk Score
                fig2 = px.scatter(analysis_df, x='Average_Attendance', y='risk_score',
                                color='risk_level', title="Attendance vs Risk Score",
                                color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'})
                st.plotly_chart(fig2, use_container_width=True)
                
                # Institute comparison
                institute_risk = analysis_df.groupby(['institute_id', 'risk_level']).size().reset_index(name='count')
                fig4 = px.bar(institute_risk, x='institute_id', y='count', color='risk_level',
                            title="Risk Distribution by Institute",
                            color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'})
                st.plotly_chart(fig4, use_container_width=True)
            
            # Summary statistics
            st.subheader("📈 Summary Statistics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Average Test Score", f"{analysis_df['test_score'].mean():.1f}")
                st.metric("Average Attendance", f"{analysis_df['Average_Attendance'].mean():.1f}%")
            
            with col2:
                high_risk_pct = (analysis_df['risk_level'] == 'High').mean() * 100
                st.metric("High Risk Students", f"{high_risk_pct:.1f}%")
                
                medium_risk_pct = (analysis_df['risk_level'] == 'Medium').mean() * 100
                st.metric("Medium Risk Students", f"{medium_risk_pct:.1f}%")
            
            with col3:
                low_risk_pct = (analysis_df['risk_level'] == 'Low').mean() * 100
                st.metric("Low Risk Students", f"{low_risk_pct:.1f}%")
                
                avg_risk_score = analysis_df['risk_score'].mean()
                st.metric("Average Risk Score", f"{avg_risk_score:.2f}")

def about_system():
    st.header("ℹ️ About the System")
    
    st.markdown("""
    ## 🎯 Smart India Hackathon 2025 Project
    
    **AI-based Dropout Prediction and Counseling System**
    
    ### 🚀 System Overview
    This system uses machine learning to predict student dropout risk based on:
    - **Attendance patterns** - Weekly attendance tracking
    - **Academic performance** - Test scores and performance trends
    - **Behavioral indicators** - Attendance decline patterns
    - **Demographic factors** - Student, mentor, and parent information
    
    ### 🤖 Machine Learning Models
    - **Decision Tree Classifier** - 99.9% accuracy
    - **Logistic Regression** - 99.6% accuracy
    - **Feature Engineering** - Advanced preprocessing pipeline
    - **Risk Scoring** - Probability-based risk assessment
    
    ### 📊 Risk Categories
    - 🟢 **Low Risk (0-30%)** - Student performing well
    - 🟡 **Medium Risk (30-70%)** - Requires monitoring
    - 🔴 **High Risk (70-100%)** - Immediate intervention needed
    
    ### 🛠️ Technology Stack
    - **Backend**: Flask API with scikit-learn models
    - **Frontend**: Streamlit dashboard
    - **ML Pipeline**: pandas, numpy, joblib
    - **Visualization**: Plotly, matplotlib
    
    ### 👥 Team Structure
    - **Data Engineers** - Raw data processing and cleaning
    - **ML Engineers** - Model development and training
    - **Backend Developers** - API development and integration
    - **Frontend Developers** - Dashboard and user interface
    - **Notification Engineers** - Alert systems and communication
    
    ### 🎯 Key Features
    - **Real-time Predictions** - Instant risk assessment
    - **Batch Processing** - Analyze multiple students
    - **Interactive Dashboard** - User-friendly interface
    - **Risk Visualization** - Charts and gauges
    - **Actionable Insights** - Specific recommendations
    
    ### 📈 Impact
    - **Early Warning System** - Identify at-risk students
    - **Intervention Planning** - Targeted support strategies
    - **Resource Optimization** - Focus efforts where needed
    - **Improved Outcomes** - Reduce dropout rates
    """)
    
    # System architecture
    st.subheader("🏗️ System Architecture")
    
    architecture_data = {
        'Component': ['Data Layer', 'ML Layer', 'API Layer', 'Frontend Layer', 'Notification Layer'],
        'Technology': ['CSV Files, SQLite', 'scikit-learn, pandas', 'Flask, REST API', 'Streamlit', 'Email/SMS'],
        'Purpose': ['Data Storage', 'Predictions', 'Backend Services', 'User Interface', 'Alerts']
    }
    
    arch_df = pd.DataFrame(architecture_data)
    st.table(arch_df)

if __name__ == "__main__":
    main()