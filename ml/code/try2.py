
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report, accuracy_score
import joblib
import matplotlib.pyplot as plt

# ========== Load CSV Data ==========
def load_data():
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

    return scores, students, parents, mentors, attendance

# ========== Feature Engineering ==========
def prepare_dataset(scores, students, parents, mentors, attendance):
    # Aggregate student scores
    score_summary = scores.groupby("student_id").agg({
        "test_score": "mean",
        "max_score": "mean"
    }).reset_index()
    score_summary["avg_score_ratio"] = score_summary["test_score"] / score_summary["max_score"]

    # Merge with student info
    df = students.merge(score_summary, on="student_id", how="left")

    # Merge attendance (row-wise, but attendance also has student_id, mentor_id, parent_id)
    # Drop duplicate columns from attendance before concatenating, but keep institute_id for later merge
    attendance_clean = attendance.drop(columns=['student_id', 'mentor_id', 'parent_id'], errors='ignore')
    df = pd.concat([df.reset_index(drop=True), attendance_clean.reset_index(drop=True)], axis=1)

    # ---- Fix mentor_id duplication ----
    # Ensure mentors DataFrame has unique columns before merging
    mentors_clean = mentors.copy()
    mentors_clean = mentors_clean.rename(columns={"mentor_id": "mentor_id_m"})
    df = df.merge(mentors_clean, left_on="mentor_id", right_on="mentor_id_m", how="left")
    df = df.drop(columns=["mentor_id_m"])  # drop helper key

    # Merge with parent info
    parents = parents.rename(columns={"parent_id": "parent_id_p"})
    df = df.merge(parents, left_on=["student_id", "parent_id"],
                         right_on=["student_id", "parent_id_p"],
                         how="left")
    df = df.drop(columns=["parent_id_p"])

    # Encode categorical columns
    le = LabelEncoder()
    for col in ["student_name", "mentor_name", "parent_name", "subject_name"]:
        if col in df.columns:
            df[col] = df[col].astype(str).fillna("Unknown")
            df[col] = le.fit_transform(df[col])

    # Clean up duplicate institute_id columns
    if 'institute_id_x' in df.columns:
        df = df.drop(columns=['institute_id_x', 'institute_id_y'])
    
    # Fill missing numeric values
    df = df.fillna(0)

    return df

def train_model(df):
    # Target - convert Yes/No to 1/0
    y = (df["Is_Declining_Attendance"] == "Yes").astype(int)

    # Drop IDs and target
    drop_cols = ["student_id", "mentor_id", "parent_id", "institute_id", "Is_Declining_Attendance"]
    X = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Logistic Regression
    log_model = LogisticRegression(max_iter=1000)
    log_model.fit(X_train, y_train)
    y_pred_log = log_model.predict(X_test)
    print("\n=== Logistic Regression ===")
    print("Accuracy:", accuracy_score(y_test, y_pred_log))
    print(classification_report(y_test, y_pred_log))

    # Decision Tree
    tree_model = DecisionTreeClassifier(max_depth=5, random_state=42)
    tree_model.fit(X_train, y_train)
    y_pred_tree = tree_model.predict(X_test)
    print("\n=== Decision Tree ===")
    print("Accuracy:", accuracy_score(y_test, y_pred_tree))
    print(classification_report(y_test, y_pred_tree))

    # Save models
    joblib.dump(log_model, "logistic_model.pkl")
    joblib.dump(tree_model, "decision_tree_model.pkl")
    joblib.dump(scaler, "scaler.pkl")
    print("✅ Models saved: logistic_model.pkl, decision_tree_model.pkl, scaler.pkl")

    # Plot Decision Tree for interpretation
    plt.figure(figsize=(16, 8))
    plot_tree(tree_model, filled=True, feature_names=X.columns.tolist(), class_names=["No Decline", "Decline"])
    plt.title("Decision Tree for Attendance Prediction")
    plt.show()

# ========== Risk Prediction Function ==========
def predict_risk(new_data, model_type="logistic"):
    """
    Predict risk of declining attendance for new students
    
    Args:
        new_data: DataFrame with student information
        model_type: "logistic" or "tree"
    
    Returns:
        DataFrame with predictions and risk scores
    """
    # Load the trained models
    try:
        if model_type == "logistic":
            model = joblib.load("logistic_model.pkl")
        else:
            model = joblib.load("decision_tree_model.pkl")
        scaler = joblib.load("scaler.pkl")
    except FileNotFoundError:
        print("❌ Model files not found. Please train the model first.")
        return None
    
    # Prepare the data (same preprocessing as training)
    df_pred = new_data.copy()
    
    # If new_data has the same structure as training data, process it
    if 'student_id' in df_pred.columns:
        # Encode categorical columns (same as training)
        le = LabelEncoder()
        for col in ["student_name", "mentor_name", "parent_name"]:
            if col in df_pred.columns:
                df_pred[col] = df_pred[col].astype(str).fillna("Unknown")
                # Note: In production, you should save the fitted label encoders
                df_pred[col] = le.fit_transform(df_pred[col])
        
        # Fill missing values
        df_pred = df_pred.fillna(0)
        
        # Drop ID columns for prediction
        drop_cols = ["student_id", "mentor_id", "parent_id", "institute_id"]
        X_pred = df_pred.drop(columns=[c for c in drop_cols if c in df_pred.columns])
        
        # Scale features
        X_pred_scaled = scaler.transform(X_pred)
        
        # Make predictions
        predictions = model.predict(X_pred_scaled)
        probabilities = model.predict_proba(X_pred_scaled)
        
        # Create results DataFrame
        results = new_data.copy()
        results['Risk_Prediction'] = predictions
        results['Risk_Score'] = probabilities[:, 1]  # Probability of declining attendance
        results['Risk_Level'] = results['Risk_Score'].apply(
            lambda x: 'High' if x > 0.7 else 'Medium' if x > 0.3 else 'Low'
        )
        
        return results
    else:
        print("❌ Input data should contain student information columns")
        return None

def demo_prediction():
    """Demonstrate prediction on sample data"""
    print("\n" + "="*50)
    print("RISK PREDICTION DEMO")
    print("="*50)
    
    # Create sample new student data
    sample_data = pd.DataFrame({
        'student_id': [999001, 999002, 999003],
        'student_name': ['John Doe', 'Jane Smith', 'Bob Wilson'],
        'mentor_id': [200001, 200002, 200003],
        'parent_id': [300001, 300002, 300003],
        'institute_id': [1, 1, 2],
        'test_score': [85, 45, 92],
        'max_score': [100, 100, 100],
        'avg_score_ratio': [0.85, 0.45, 0.92],
        'Week_1_Attendance': [95, 60, 100],
        'Week_2_Attendance': [90, 55, 98],
        'Week_3_Attendance': [88, 50, 95],
        'Week_4_Attendance': [85, 45, 92],
        'Week_5_Attendance': [82, 40, 90],
        'Week_6_Attendance': [80, 35, 88],
        'Week_7_Attendance': [78, 30, 85],
        'Week_8_Attendance': [75, 25, 82],
        'Week_9_Attendance': [72, 20, 80],
        'Week_10_Attendance': [70, 15, 78],
        'Week_11_Attendance': [68, 10, 75],
        'Week_12_Attendance': [65, 5, 72],
        'Attendance_Decline_Score': [5.0, 15.0, 2.0],
        'Is_Declining_Attendance': ['No', 'Yes', 'No'],  # This won't be used for prediction
        'Average_Attendance': [78.3, 32.5, 86.5],
        'Lowest_Week_Attendance': [65, 5, 72],
        'Highest_Week_Attendance': [95, 60, 100],
        'mentor_name': ['Anjali Mehta', 'Shreya Sastry', 'Pradeep Ghosh'],
        'parent_name': ['Sunita Hussain', 'Asha Malhotra', 'Riya Reddy']
    })
    
    print("Sample Student Data:")
    print(sample_data[['student_id', 'student_name', 'Average_Attendance', 'Attendance_Decline_Score']].to_string(index=False))
    
    # Predict using Logistic Regression
    print("\n🔍 Predicting with Logistic Regression...")
    results_lr = predict_risk(sample_data, model_type="logistic")
    if results_lr is not None:
        print("\nLogistic Regression Results:")
        print(results_lr[['student_name', 'Risk_Prediction', 'Risk_Score', 'Risk_Level']].to_string(index=False))
    
    # Predict using Decision Tree
    print("\n🌳 Predicting with Decision Tree...")
    results_tree = predict_risk(sample_data, model_type="tree")
    if results_tree is not None:
        print("\nDecision Tree Results:")
        print(results_tree[['student_name', 'Risk_Prediction', 'Risk_Score', 'Risk_Level']].to_string(index=False))

# ========== Run ==========
if __name__ == "__main__":
    print("🚀 STARTING ATTENDANCE RISK PREDICTION SYSTEM")
    print("="*60)
    
    print("\n📊 Step 1: Loading data...")
    scores, students, parents, mentors, attendance = load_data()
    print(f"Data loaded - Scores: {scores.shape}, Students: {students.shape}, Parents: {parents.shape}, Mentors: {mentors.shape}, Attendance: {attendance.shape}")
    
    print("\n🔧 Step 2: Preparing dataset...")
    df = prepare_dataset(scores, students, parents, mentors, attendance)
    print("Final dataset shape:", df.shape)
    print("Columns:", df.columns.tolist())
    
    print("\n🤖 Step 3: Training models...")
    train_model(df)
    
    print("\n🎯 Step 4: Demonstrating risk prediction...")
    demo_prediction()
    
    print("\n✅ SYSTEM READY FOR RISK PREDICTION!")
    print("="*60)
