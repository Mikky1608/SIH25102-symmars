import pandas as pd
import numpy as np

def create_comprehensive_dataset():
    """Create a comprehensive CSV dataset from all source files"""
    print("📊 Creating comprehensive dataset...")
    
    # Load all data sources
    print("Loading data sources...")
    
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

    print(f"Data loaded:")
    print(f"  - Scores: {scores.shape[0]} records")
    print(f"  - Students: {students.shape[0]} records")
    print(f"  - Parents: {parents.shape[0]} records")
    print(f"  - Mentors: {mentors.shape[0]} records")
    print(f"  - Attendance: {attendance.shape[0]} records")

    # Aggregate scores by student
    print("Aggregating academic scores...")
    score_summary = scores.groupby("student_id").agg({
        "test_score": ["mean", "std", "min", "max", "count"],
        "max_score": "mean"
    }).reset_index()
    
    # Flatten column names
    score_summary.columns = [
        'student_id', 'avg_test_score', 'std_test_score', 'min_test_score', 
        'max_test_score', 'test_count', 'avg_max_score'
    ]
    
    # Calculate performance ratio
    score_summary["avg_score_ratio"] = score_summary["avg_test_score"] / score_summary["avg_max_score"]
    
    # Start with student base data
    print("Merging datasets...")
    dataset = students.copy()
    
    # Add academic performance
    dataset = dataset.merge(score_summary, on="student_id", how="left")
    
    # Add attendance data
    attendance_cols = [
        'Week_1_Attendance', 'Week_2_Attendance', 'Week_3_Attendance',
        'Week_4_Attendance', 'Week_5_Attendance', 'Week_6_Attendance',
        'Week_7_Attendance', 'Week_8_Attendance', 'Week_9_Attendance',
        'Week_10_Attendance', 'Week_11_Attendance', 'Week_12_Attendance',
        'Attendance_Decline_Score', 'Is_Declining_Attendance',
        'Average_Attendance', 'Lowest_Week_Attendance', 'Highest_Week_Attendance'
    ]
    
    attendance_data = attendance[['student_id'] + attendance_cols]
    dataset = dataset.merge(attendance_data, on="student_id", how="left")
    
    # Add parent information
    parent_data = parents[['student_id', 'parent_name']].rename(columns={'parent_name': 'parent_name'})
    dataset = dataset.merge(parent_data, on="student_id", how="left")
    
    # Add mentor information
    mentor_data = mentors[['mentor_id', 'mentor_name']]
    dataset = dataset.merge(mentor_data, on="mentor_id", how="left")
    
    # Fill missing values
    dataset = dataset.fillna({
        'avg_test_score': 0,
        'std_test_score': 0,
        'min_test_score': 0,
        'max_test_score': 0,
        'test_count': 0,
        'avg_max_score': 100,
        'avg_score_ratio': 0,
        'parent_name': 'Unknown',
        'mentor_name': 'Unknown'
    })
    
    # Fill attendance missing values
    attendance_numeric_cols = [col for col in attendance_cols if 'Week' in col or 'Attendance' in col]
    for col in attendance_numeric_cols:
        if col in dataset.columns:
            dataset[col] = dataset[col].fillna(0)
    
    # Fill categorical attendance
    dataset['Is_Declining_Attendance'] = dataset['Is_Declining_Attendance'].fillna('No')
    
    # Create risk target variable
    dataset['Risk_Target'] = (dataset['Is_Declining_Attendance'] == 'Yes').astype(int)
    
    # Reorder columns for better readability
    column_order = [
        'student_id', 'student_name', 'institute_id', 'mentor_id', 'mentor_name', 
        'parent_id', 'parent_name',
        'avg_test_score', 'std_test_score', 'min_test_score', 'max_test_score', 
        'test_count', 'avg_max_score', 'avg_score_ratio',
        'Week_1_Attendance', 'Week_2_Attendance', 'Week_3_Attendance',
        'Week_4_Attendance', 'Week_5_Attendance', 'Week_6_Attendance',
        'Week_7_Attendance', 'Week_8_Attendance', 'Week_9_Attendance',
        'Week_10_Attendance', 'Week_11_Attendance', 'Week_12_Attendance',
        'Average_Attendance', 'Lowest_Week_Attendance', 'Highest_Week_Attendance',
        'Attendance_Decline_Score', 'Is_Declining_Attendance', 'Risk_Target'
    ]
    
    # Select available columns in order
    available_columns = [col for col in column_order if col in dataset.columns]
    dataset = dataset[available_columns]
    
    print(f"Final dataset shape: {dataset.shape}")
    print(f"Columns: {len(dataset.columns)}")
    
    # Save to CSV
    output_file = "../comprehensive_student_dataset.csv"
    dataset.to_csv(output_file, index=False, encoding='utf-8')
    print(f"✅ Dataset saved to: {output_file}")
    
    # Print summary statistics
    print("\n📊 Dataset Summary:")
    print(f"  Total Students: {len(dataset):,}")
    print(f"  Institute 1: {len(dataset[dataset['institute_id'] == 1]):,}")
    print(f"  Institute 2: {len(dataset[dataset['institute_id'] == 2]):,}")
    print(f"  At Risk: {len(dataset[dataset['Risk_Target'] == 1]):,} ({len(dataset[dataset['Risk_Target'] == 1])/len(dataset)*100:.1f}%)")
    print(f"  Not At Risk: {len(dataset[dataset['Risk_Target'] == 0]):,} ({len(dataset[dataset['Risk_Target'] == 0])/len(dataset)*100:.1f}%)")
    
    print(f"\n📈 Academic Performance:")
    print(f"  Average Test Score: {dataset['avg_test_score'].mean():.2f}")
    print(f"  Average Score Ratio: {dataset['avg_score_ratio'].mean():.3f}")
    
    print(f"\n📅 Attendance Statistics:")
    print(f"  Average Attendance: {dataset['Average_Attendance'].mean():.2f}%")
    print(f"  Average Decline Score: {dataset['Attendance_Decline_Score'].mean():.2f}")
    
    return dataset

if __name__ == "__main__":
    dataset = create_comprehensive_dataset()
    print("\n✅ Comprehensive dataset creation complete!")