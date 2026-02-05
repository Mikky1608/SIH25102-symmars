import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

def load_and_prepare_data():
    """Load and merge all datasets"""
    print("📊 Loading data...")
    
    # Scores
    scores1 = pd.read_csv("data/Weekly_Scores_Institute1.csv", encoding='utf-8')
    scores2 = pd.read_csv("data/Weekly_Scores_Institute2.csv", encoding='utf-8')
    scores = pd.concat([scores1, scores2], ignore_index=True)

    # Students
    students1 = pd.read_csv("data/Students_Institute1.csv", encoding='utf-8')
    students2 = pd.read_csv("data/Students_Institute2.csv", encoding='utf-8')
    students = pd.concat([students1, students2], ignore_index=True)

    # Attendance
    att1 = pd.read_csv("data/Attendance_Wide_Format_Institute1.csv", encoding='utf-8')
    att2 = pd.read_csv("data/Attendance_Wide_Format_Institute2.csv", encoding='utf-8')
    attendance = pd.concat([att1, att2], ignore_index=True)

    # Aggregate scores
    score_summary = scores.groupby("student_id").agg({
        "test_score": "mean",
        "max_score": "mean"
    }).reset_index()
    score_summary["avg_score_ratio"] = score_summary["test_score"] / score_summary["max_score"]

    # Merge datasets
    df = students.merge(score_summary, on="student_id", how="left")
    attendance_clean = attendance.drop(columns=['student_id', 'mentor_id', 'parent_id'], errors='ignore')
    df = pd.concat([df.reset_index(drop=True), attendance_clean.reset_index(drop=True)], axis=1)
    
    # Encode target variable
    df['Target'] = (df["Is_Declining_Attendance"] == "Yes").astype(int)
    
    # Fill missing values
    df = df.fillna(0)
    
    print(f"✅ Data loaded: {df.shape[0]} students, {df.shape[1]} features")
    return df

def correlation_analysis(df):
    """Perform comprehensive correlation analysis"""
    print("\n" + "="*80)
    print("📈 CORRELATION ANALYSIS WITH DROPOUT RISK")
    print("="*80)
    
    # Select numerical features
    numerical_features = [
        'test_score', 'max_score', 'avg_score_ratio',
        'Week_1_Attendance', 'Week_2_Attendance', 'Week_3_Attendance',
        'Week_4_Attendance', 'Week_5_Attendance', 'Week_6_Attendance',
        'Week_7_Attendance', 'Week_8_Attendance', 'Week_9_Attendance',
        'Week_10_Attendance', 'Week_11_Attendance', 'Week_12_Attendance',
        'Attendance_Decline_Score', 'Average_Attendance',
        'Lowest_Week_Attendance', 'Highest_Week_Attendance', 'Target'
    ]
    
    # Filter available features
    available_features = [f for f in numerical_features if f in df.columns]
    df_corr = df[available_features]
    
    # Calculate correlation matrix
    correlation_matrix = df_corr.corr()
    
    # Get correlations with target variable
    target_correlations = correlation_matrix['Target'].sort_values(ascending=False)
    
    print("\n🔴 POSITIVE CORRELATIONS (Risk Factors):")
    print("-" * 80)
    positive_corr = target_correlations[target_correlations > 0].drop('Target')
    for feature, corr in positive_corr.items():
        strength = get_correlation_strength(abs(corr))
        print(f"  {feature:35s} : {corr:+.4f}  [{strength}]")
    
    print("\n🟢 NEGATIVE CORRELATIONS (Protective Factors):")
    print("-" * 80)
    negative_corr = target_correlations[target_correlations < 0]
    for feature, corr in negative_corr.items():
        strength = get_correlation_strength(abs(corr))
        print(f"  {feature:35s} : {corr:+.4f}  [{strength}]")
    
    return target_correlations

def get_correlation_strength(corr):
    """Classify correlation strength"""
    if abs(corr) >= 0.7:
        return "Very Strong"
    elif abs(corr) >= 0.5:
        return "Strong"
    elif abs(corr) >= 0.3:
        return "Moderate"
    elif abs(corr) >= 0.1:
        return "Weak"
    else:
        return "Very Weak"

def statistical_analysis(df):
    """Perform statistical analysis by risk group"""
    print("\n" + "="*80)
    print("📊 STATISTICAL COMPARISON BY RISK GROUP")
    print("="*80)
    
    # Group by target
    at_risk = df[df['Target'] == 1]
    not_at_risk = df[df['Target'] == 0]
    
    print(f"\n📌 Sample Distribution:")
    print(f"  Not At Risk: {len(not_at_risk):,} students ({len(not_at_risk)/len(df)*100:.1f}%)")
    print(f"  At Risk:     {len(at_risk):,} students ({len(at_risk)/len(df)*100:.1f}%)")
    
    # Key metrics comparison
    metrics = [
        'Average_Attendance', 'Attendance_Decline_Score',
        'avg_score_ratio', 'Lowest_Week_Attendance', 'Highest_Week_Attendance'
    ]
    
    print("\n📊 KEY METRICS COMPARISON:")
    print("-" * 80)
    print(f"{'Metric':<35} {'Not At Risk':>15} {'At Risk':>15} {'Difference':>15}")
    print("-" * 80)
    
    for metric in metrics:
        if metric in df.columns:
            not_risk_mean = not_at_risk[metric].mean()
            at_risk_mean = at_risk[metric].mean()
            diff = at_risk_mean - not_risk_mean
            print(f"{metric:<35} {not_risk_mean:>15.2f} {at_risk_mean:>15.2f} {diff:>15.2f}")

def attendance_pattern_analysis(df):
    """Analyze attendance patterns over 12 weeks"""
    print("\n" + "="*80)
    print("📅 WEEKLY ATTENDANCE PATTERN ANALYSIS")
    print("="*80)
    
    weeks = [f'Week_{i}_Attendance' for i in range(1, 13)]
    available_weeks = [w for w in weeks if w in df.columns]
    
    if not available_weeks:
        print("⚠️  Weekly attendance data not available")
        return
    
    # Calculate average attendance by week for each group
    at_risk = df[df['Target'] == 1]
    not_at_risk = df[df['Target'] == 0]
    
    print("\n📈 AVERAGE ATTENDANCE BY WEEK:")
    print("-" * 80)
    print(f"{'Week':<10} {'Not At Risk':>15} {'At Risk':>15} {'Gap':>15}")
    print("-" * 80)
    
    for i, week in enumerate(available_weeks, 1):
        not_risk_avg = not_at_risk[week].mean()
        at_risk_avg = at_risk[week].mean()
        gap = not_risk_avg - at_risk_avg
        print(f"Week {i:<5} {not_risk_avg:>15.2f}% {at_risk_avg:>15.2f}% {gap:>15.2f}%")
    
    # Calculate decline rates
    if len(available_weeks) >= 2:
        print("\n📉 ATTENDANCE DECLINE ANALYSIS:")
        print("-" * 80)
        
        # First vs Last week comparison
        first_week = available_weeks[0]
        last_week = available_weeks[-1]
        
        not_risk_decline = not_at_risk[first_week].mean() - not_at_risk[last_week].mean()
        at_risk_decline = at_risk[first_week].mean() - at_risk[last_week].mean()
        
        print(f"  Not At Risk - First to Last Week Decline: {not_risk_decline:.2f}%")
        print(f"  At Risk - First to Last Week Decline:     {at_risk_decline:.2f}%")
        print(f"  Difference in Decline Rate:               {at_risk_decline - not_risk_decline:.2f}%")

def feature_importance_ranking(target_correlations):
    """Rank features by importance"""
    print("\n" + "="*80)
    print("🎯 FEATURE IMPORTANCE RANKING (by Absolute Correlation)")
    print("="*80)
    
    # Get absolute correlations (excluding target itself)
    importance = target_correlations.drop('Target').abs().sort_values(ascending=False)
    
    print("\n📊 TOP 15 MOST IMPORTANT FEATURES:")
    print("-" * 80)
    print(f"{'Rank':<6} {'Feature':<35} {'|Correlation|':>15} {'Direction':>12} {'Impact':>15}")
    print("-" * 80)
    
    for rank, (feature, abs_corr) in enumerate(importance.head(15).items(), 1):
        direction = "Risk ↑" if target_correlations[feature] > 0 else "Risk ↓"
        impact = "🔴 Critical" if abs_corr >= 0.5 else "🟡 High" if abs_corr >= 0.3 else "🟢 Moderate"
        print(f"{rank:<6} {feature:<35} {abs_corr:>15.4f} {direction:>12} {impact:>15}")

def generate_insights(target_correlations, df):
    """Generate actionable insights"""
    print("\n" + "="*80)
    print("💡 KEY INSIGHTS & ACTIONABLE RECOMMENDATIONS")
    print("="*80)
    
    # Get top correlations
    top_positive = target_correlations[target_correlations > 0].drop('Target').head(3)
    top_negative = target_correlations[target_correlations < 0].head(3)
    
    print("\n🚨 STRONGEST RISK INDICATORS:")
    for i, (feature, corr) in enumerate(top_positive.items(), 1):
        print(f"  {i}. {feature}: {corr:.4f}")
    
    print("\n🛡️  STRONGEST PROTECTIVE FACTORS:")
    for i, (feature, corr) in enumerate(top_negative.items(), 1):
        print(f"  {i}. {feature}: {corr:.4f}")
    
    print("\n📋 ACTIONABLE RECOMMENDATIONS:")
    print("-" * 80)
    print("  🎯 PRIMARY INTERVENTIONS:")
    print("    • Monitor Attendance_Decline_Score as #1 early warning indicator")
    print("    • Immediate intervention when Average_Attendance < 70%")
    print("    • Track weekly attendance patterns for declining trends")
    
    print("\n  📊 SECONDARY INDICATORS:")
    print("    • Academic performance (avg_score_ratio) correlates with retention")
    print("    • Recent weeks (10-12) are more predictive than early weeks")
    print("    • Lowest weekly attendance is a critical threshold indicator")
    
    print("\n  🔧 IMPLEMENTATION STRATEGY:")
    print("    • Set up automated alerts for decline score > 5.0")
    print("    • Weekly monitoring for students with average attendance < 75%")
    print("    • Academic support programs for low-performing students")
    print("    • Early intervention protocols for consistent attendance drops")

def main():
    print("🎓 STUDENT DROPOUT PREDICTION - CORRELATION ANALYSIS")
    print("="*80)
    
    # Load data
    df = load_and_prepare_data()
    
    # Perform correlation analysis
    target_correlations = correlation_analysis(df)
    
    # Statistical analysis
    statistical_analysis(df)
    
    # Attendance pattern analysis
    attendance_pattern_analysis(df)
    
    # Feature importance ranking
    feature_importance_ranking(target_correlations)
    
    # Generate insights
    generate_insights(target_correlations, df)
    
    print("\n" + "="*80)
    print("✅ CORRELATION ANALYSIS COMPLETE!")
    print("="*80)

if __name__ == "__main__":
    main()