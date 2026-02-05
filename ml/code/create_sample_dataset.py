import pandas as pd
import numpy as np

def create_sample_dataset():
    """Create a smaller sample dataset for testing"""
    print("📊 Creating sample dataset from comprehensive data...")
    
    # Load the comprehensive dataset
    df = pd.read_csv("../comprehensive_student_dataset.csv")
    
    # Sample strategy: get representative samples from each risk group
    at_risk = df[df['Risk_Target'] == 1]
    not_at_risk = df[df['Risk_Target'] == 0]
    
    print(f"Original dataset: {len(df)} students")
    print(f"  At Risk: {len(at_risk)} students")
    print(f"  Not At Risk: {len(not_at_risk)} students")
    
    # Sample 25 at-risk and 75 not-at-risk students for a balanced representation
    sample_at_risk = at_risk.sample(n=min(25, len(at_risk)), random_state=42)
    sample_not_at_risk = not_at_risk.sample(n=min(75, len(not_at_risk)), random_state=42)
    
    # Combine samples
    sample_df = pd.concat([sample_at_risk, sample_not_at_risk], ignore_index=True)
    
    # Shuffle the dataset
    sample_df = sample_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Select key columns for easier use
    key_columns = [
        'student_id', 'student_name', 'institute_id',
        'avg_test_score', 'avg_score_ratio',
        'Week_1_Attendance', 'Week_2_Attendance', 'Week_3_Attendance',
        'Week_4_Attendance', 'Week_5_Attendance', 'Week_6_Attendance',
        'Week_7_Attendance', 'Week_8_Attendance', 'Week_9_Attendance',
        'Week_10_Attendance', 'Week_11_Attendance', 'Week_12_Attendance',
        'Average_Attendance', 'Lowest_Week_Attendance', 'Highest_Week_Attendance',
        'Attendance_Decline_Score', 'Is_Declining_Attendance', 'Risk_Target'
    ]
    
    sample_df = sample_df[key_columns]
    
    # Rename columns for API compatibility
    sample_df = sample_df.rename(columns={
        'avg_test_score': 'test_score',
        'avg_score_ratio': 'avg_score_ratio'
    })
    
    # Save sample dataset
    output_file = "../sample_student_dataset.csv"
    sample_df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n✅ Sample dataset saved to: {output_file}")
    print(f"Sample dataset shape: {sample_df.shape}")
    print(f"  At Risk: {len(sample_df[sample_df['Risk_Target'] == 1])} students")
    print(f"  Not At Risk: {len(sample_df[sample_df['Risk_Target'] == 0])} students")
    
    # Show first few rows
    print(f"\n📋 Sample Data Preview:")
    print(sample_df[['student_id', 'student_name', 'Average_Attendance', 'Attendance_Decline_Score', 'Is_Declining_Attendance']].head(10).to_string(index=False))
    
    return sample_df

if __name__ == "__main__":
    sample_df = create_sample_dataset()
    print("\n✅ Sample dataset creation complete!")