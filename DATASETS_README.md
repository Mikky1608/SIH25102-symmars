# 📊 Student Dropout Prediction - Dataset Documentation

## 📁 Available Datasets

### 1. **comprehensive_student_dataset.csv** (Full Dataset)
**Size**: 4,000 students  
**Purpose**: Complete dataset with all features for training and analysis

#### **Contents:**
- **4,000 students** from 2 institutes
- **32 features** including demographics, academic performance, and attendance
- **425 at-risk students** (10.6%)
- **3,575 not-at-risk students** (89.4%)

#### **Key Statistics:**
- Average Test Score: 76.80
- Average Score Ratio: 0.768
- Average Attendance: 80.25%
- Average Decline Score: 3.54

#### **Columns:**
```
student_id, student_name, student_email, institute_id, mentor_id, mentor_name, 
parent_id, parent_name, avg_test_score, std_test_score, 
min_test_score, max_test_score, test_count, avg_max_score, 
avg_score_ratio, Week_1_Attendance, Week_2_Attendance, ..., 
Week_12_Attendance, Average_Attendance, Lowest_Week_Attendance, 
Highest_Week_Attendance, Attendance_Decline_Score, 
Is_Declining_Attendance, Risk_Target
```

---

### 2. **sample_student_dataset.csv** (Sample Dataset)
**Size**: 100 students  
**Purpose**: Smaller dataset for quick testing and demonstrations

#### **Contents:**
- **100 students** (representative sample)
- **23 key features** (simplified for easier use)
- **25 at-risk students** (25%)
- **75 not-at-risk students** (75%)

#### **Columns:**
```
student_id, student_name, student_email, institute_id, test_score, avg_score_ratio,
Week_1_Attendance, Week_2_Attendance, ..., Week_12_Attendance,
Average_Attendance, Lowest_Week_Attendance, Highest_Week_Attendance,
Attendance_Decline_Score, Is_Declining_Attendance, Risk_Target
```

---

### 3. **sample_batch_students.csv** (Demo Dataset)
**Size**: 10 students  
**Purpose**: Quick demo file for testing batch prediction feature

#### **Contents:**
- **10 students** with diverse risk profiles
- **3 High Risk** students
- **4 Medium Risk** students
- **3 Low Risk** students

#### **Use Case:**
Perfect for demonstrating the batch prediction feature in the web dashboard.

---

## 🎯 How to Use These Datasets

### **For Web Dashboard (Streamlit)**

#### **Option 1: Use Sample Dataset (Recommended for Testing)**
1. Open http://localhost:8501
2. Go to "Batch Prediction"
3. Upload `sample_student_dataset.csv`
4. Click "Predict All Students"
5. View results and download predictions

#### **Option 2: Use Demo Dataset (Quick Test)**
1. Open http://localhost:8501
2. Go to "Batch Prediction"
3. Upload `sample_batch_students.csv`
4. Click "Predict All Students"
5. See immediate results with 10 students

#### **Option 3: Use Full Dataset (Complete Analysis)**
1. Open http://localhost:8501
2. Go to "Batch Prediction"
3. Upload `comprehensive_student_dataset.csv`
4. Click "Predict All Students"
5. Analyze all 4,000 students

### **For API Integration**

#### **Single Student Prediction**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 100001,
    "student_name": "John Doe",
    "institute_id": 1,
    "test_score": 75,
    "Average_Attendance": 65.5,
    "Attendance_Decline_Score": 12.5
  }'
```

#### **Batch Prediction (PowerShell)**
```powershell
# Convert CSV to JSON and send to API
$csv = Import-Csv "sample_student_dataset.csv"
$json = $csv | ConvertTo-Json
$body = @{ students = $csv } | ConvertTo-Json -Depth 10
Invoke-WebRequest -Uri "http://localhost:5000/predict-batch" `
  -Method POST -ContentType "application/json" -Body $body
```

---

## 📋 Column Descriptions

### **Student Information**
- `student_id`: Unique student identifier
- `student_name`: Student's full name
- `student_email`: Student's Gmail address (firstname.lastname@gmail.com format)
- `institute_id`: Institute identifier (1 or 2)
- `mentor_id`: Assigned mentor identifier
- `mentor_name`: Mentor's name
- `parent_id`: Parent/guardian identifier
- `parent_name`: Parent/guardian name

### **Academic Performance**
- `test_score` / `avg_test_score`: Average test score across all subjects
- `std_test_score`: Standard deviation of test scores
- `min_test_score`: Minimum test score
- `max_test_score`: Maximum test score
- `test_count`: Number of tests taken
- `avg_max_score`: Average maximum possible score
- `avg_score_ratio`: Performance ratio (test_score / max_score)

### **Weekly Attendance (12 weeks)**
- `Week_1_Attendance` to `Week_12_Attendance`: Weekly attendance percentage

### **Attendance Metrics**
- `Average_Attendance`: Overall average attendance percentage
- `Lowest_Week_Attendance`: Minimum weekly attendance
- `Highest_Week_Attendance`: Maximum weekly attendance
- `Attendance_Decline_Score`: Calculated decline trend (higher = more decline)

### **Target Variables**
- `Is_Declining_Attendance`: "Yes" or "No" (categorical)
- `Risk_Target`: 1 (At Risk) or 0 (Not At Risk) (binary)

---

## 🔍 Data Quality & Preprocessing

### **Data Cleaning Applied:**
- Missing values filled with appropriate defaults (0 for numeric, "Unknown" for categorical)
- Attendance percentages validated (0-100 range)
- Academic scores normalized to ratios
- Categorical variables encoded for ML models

### **Feature Engineering:**
- `avg_score_ratio`: Calculated from test_score / max_score
- `Attendance_Decline_Score`: Derived from weekly attendance patterns
- `Average_Attendance`: Mean of all 12 weekly attendance values
- `Lowest_Week_Attendance`: Minimum across all weeks
- `Highest_Week_Attendance`: Maximum across all weeks

---

## 📊 Dataset Statistics

### **Risk Distribution**
| Dataset | Total | At Risk | Not At Risk | Risk % |
|---------|-------|---------|-------------|--------|
| Comprehensive | 4,000 | 425 | 3,575 | 10.6% |
| Sample | 100 | 25 | 75 | 25.0% |
| Demo | 10 | 3 | 7 | 30.0% |

### **Institute Distribution**
| Institute | Students | Percentage |
|-----------|----------|------------|
| Institute 1 | 2,000 | 50% |
| Institute 2 | 2,000 | 50% |

### **Attendance Patterns**
| Metric | At Risk | Not At Risk | Difference |
|--------|---------|-------------|------------|
| Average Attendance | 59.85% | 82.68% | -22.83% |
| Decline Score | 34.89 | -0.19 | +35.08 |
| Lowest Week | 38.42% | 74.58% | -36.16% |

---

## 🎯 Use Case Examples

### **1. Training ML Models**
Use `comprehensive_student_dataset.csv` for:
- Training new models
- Cross-validation
- Feature importance analysis
- Model comparison

### **2. Testing & Validation**
Use `sample_student_dataset.csv` for:
- Quick model testing
- API endpoint validation
- Performance benchmarking
- Demo presentations

### **3. User Demonstrations**
Use `sample_batch_students.csv` for:
- Live demos
- User training
- Feature showcases
- Quick predictions

---

## 🔧 Creating Custom Datasets

### **From Original Data**
```bash
cd ml
python code/create_dataset.py
```
This regenerates the comprehensive dataset from source files.

### **Custom Sample Size**
Modify `create_sample_dataset.py` to change sample size:
```python
sample_at_risk = at_risk.sample(n=50, random_state=42)  # Change 50 to desired size
sample_not_at_risk = not_at_risk.sample(n=150, random_state=42)  # Change 150
```

---

## 📈 Expected Prediction Results

### **Using Decision Tree Model (99.875% accuracy)**

#### **High Risk Students (Risk Score > 0.7)**
- Attendance_Decline_Score > 15
- Average_Attendance < 60%
- Recent weeks (10-12) < 50%

#### **Medium Risk Students (Risk Score 0.3-0.7)**
- Attendance_Decline_Score 5-15
- Average_Attendance 60-75%
- Declining trend visible

#### **Low Risk Students (Risk Score < 0.3)**
- Attendance_Decline_Score < 5
- Average_Attendance > 75%
- Stable or improving attendance

---

## 📞 Support & Questions

For questions about the datasets:
1. Check the correlation analysis report: `ml/CORRELATION_ANALYSIS_REPORT.md`
2. Review the ML training code: `ml/code/try1.py`
3. See the preprocessing pipeline in the backend: `backend/app.py`

---

*Last Updated: February 2026*  
*Dataset Version: 1.0*  
*Total Records: 4,000 students*