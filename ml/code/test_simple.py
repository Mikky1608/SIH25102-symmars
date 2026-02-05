import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

print("🚀 Testing data loading...")

# Test loading data
try:
    # Scores
    scores1 = pd.read_csv("data/Weekly_Scores_Institute1.csv", encoding='utf-8')
    scores2 = pd.read_csv("data/Weekly_Scores_Institute2.csv", encoding='utf-8')
    scores = pd.concat([scores1, scores2], ignore_index=True)

    # Students
    students1 = pd.read_csv("data/Students_Institute1.csv", encoding='utf-8')
    students2 = pd.read_csv("data/Students_Institute2.csv", encoding='utf-8')
    students = pd.concat([students1, students2], ignore_index=True)

    # Parents
    parents1 = pd.read_csv("data/Parents_Institute1.csv", encoding='utf-8')
    parents2 = pd.read_csv("data/Parents_Institute2.csv", encoding='utf-8')
    parents = pd.concat([parents1, parents2], ignore_index=True)

    # Mentors
    mentors1 = pd.read_csv("data/Mentors_Institute1.csv", encoding='utf-8')
    mentors2 = pd.read_csv("data/Mentors_Institute2.csv", encoding='utf-8')
    mentors = pd.concat([mentors1, mentors2], ignore_index=True)

    # Attendance
    att1 = pd.read_csv("data/Attendance_Wide_Format_Institute1.csv", encoding='utf-8')
    att2 = pd.read_csv("data/Attendance_Wide_Format_Institute2.csv", encoding='utf-8')
    attendance = pd.concat([att1, att2], ignore_index=True)

    print(f"✅ Data loaded successfully:")
    print(f"   Scores: {scores.shape}")
    print(f"   Students: {students.shape}")
    print(f"   Parents: {parents.shape}")
    print(f"   Mentors: {mentors.shape}")
    print(f"   Attendance: {attendance.shape}")
    
except Exception as e:
    print(f"❌ Error loading data: {e}")
    import traceback
    traceback.print_exc()
