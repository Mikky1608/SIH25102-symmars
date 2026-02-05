import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# ========== Load and Prepare Data ==========
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

# ========== Correlation Analysis ==========
def correlation_analysis(df):
    """Perform comprehensive correlation analysis"""
    print("\n" + "="*70)
    print("📈 CORRELATION ANALYSIS WITH TARGET VARIABLE")
    print("="*70)
    
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
    
    print("\n🎯 TOP POSITIVE CORRELATIONS WITH DROPOUT RISK:")
    print("-" * 70)
    positive_corr = target_correlations[target_correlations > 0].drop('Target')
    for feature, corr in positive_corr.items():
        strength = get_correlation_strength(abs(corr))
        print(f"  {feature:30s} : {corr:+.4f}  [{strength}]")
    
    print("\n🎯 TOP NEGATIVE CORRELATIONS WITH DROPOUT RISK:")
    print("-" * 70)
    negative_corr = target_correlations[target_correlations < 0]
    for feature, corr in negative_corr.items():
        strength = get_correlation_strength(abs(corr))
        print(f"  {feature:30s} : {corr:+.4f}  [{strength}]")
    
    return correlation_matrix, target_correlations

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

# ========== Statistical Analysis ==========
def statistical_analysis(df):
    """Perform statistical analysis by risk group"""
    print("\n" + "="*70)
    print("📊 STATISTICAL ANALYSIS BY RISK GROUP")
    print("="*70)
    
    # Group by target
    at_risk = df[df['Target'] == 1]
    not_at_risk = df[df['Target'] == 0]
    
    print(f"\n📌 Sample Distribution:")
    print(f"  Not At Risk: {len(not_at_risk)} students ({len(not_at_risk)/len(df)*100:.1f}%)")
    print(f"  At Risk:     {len(at_risk)} students ({len(at_risk)/len(df)*100:.1f}%)")
    
    # Key metrics comparison
    metrics = [
        'Average_Attendance', 'Attendance_Decline_Score',
        'avg_score_ratio', 'Lowest_Week_Attendance'
    ]
    
    print("\n📊 KEY METRICS COMPARISON:")
    print("-" * 70)
    print(f"{'Metric':<30} {'Not At Risk':>15} {'At Risk':>15} {'Difference':>15}")
    print("-" * 70)
    
    for metric in metrics:
        if metric in df.columns:
            not_risk_mean = not_at_risk[metric].mean()
            at_risk_mean = at_risk[metric].mean()
            diff = at_risk_mean - not_risk_mean
            print(f"{metric:<30} {not_risk_mean:>15.2f} {at_risk_mean:>15.2f} {diff:>15.2f}")

# ========== Attendance Pattern Analysis ==========
def attendance_pattern_analysis(df):
    """Analyze attendance patterns over 12 weeks"""
    print("\n" + "="*70)
    print("📅 ATTENDANCE PATTERN ANALYSIS (12 WEEKS)")
    print("="*70)
    
    weeks = [f'Week_{i}_Attendance' for i in range(1, 13)]
    available_weeks = [w for w in weeks if w in df.columns]
    
    if not available_weeks:
        print("⚠️  Weekly attendance data not available")
        return
    
    # Calculate average attendance by week for each group
    at_risk = df[df['Target'] == 1]
    not_at_risk = df[df['Target'] == 0]
    
    print("\n📈 AVERAGE ATTENDANCE BY WEEK:")
    print("-" * 70)
    print(f"{'Week':<10} {'Not At Risk':>15} {'At Risk':>15} {'Gap':>15}")
    print("-" * 70)
    
    for i, week in enumerate(available_weeks, 1):
        not_risk_avg = not_at_risk[week].mean()
        at_risk_avg = at_risk[week].mean()
        gap = not_risk_avg - at_risk_avg
        print(f"Week {i:<5} {not_risk_avg:>15.2f}% {at_risk_avg:>15.2f}% {gap:>15.2f}%")
    
    # Calculate decline rates
    if len(available_weeks) >= 2:
        print("\n📉 ATTENDANCE DECLINE ANALYSIS:")
        print("-" * 70)
        
        # First vs Last week comparison
        first_week = available_weeks[0]
        last_week = available_weeks[-1]
        
        not_risk_decline = not_at_risk[first_week].mean() - not_at_risk[last_week].mean()
        at_risk_decline = at_risk[first_week].mean() - at_risk[last_week].mean()
        
        print(f"  Not At Risk - Decline: {not_risk_decline:.2f}%")
        print(f"  At Risk - Decline:     {at_risk_decline:.2f}%")
        print(f"  Difference:            {at_risk_decline - not_risk_decline:.2f}%")

# ========== Feature Importance Analysis ==========
def feature_importance_analysis(correlation_matrix, target_correlations):
    """Analyze feature importance based on correlations"""
    print("\n" + "="*70)
    print("🎯 FEATURE IMPORTANCE RANKING")
    print("="*70)
    
    # Get absolute correlations (excluding target itself)
    importance = target_correlations.drop('Target').abs().sort_values(ascending=False)
    
    print("\n📊 TOP 10 MOST IMPORTANT FEATURES:")
    print("-" * 70)
    print(f"{'Rank':<6} {'Feature':<35} {'|Correlation|':>15} {'Impact':>15}")
    print("-" * 70)
    
    for rank, (feature, corr) in enumerate(importance.head(10).items(), 1):
        impact = "🔴 Critical" if corr >= 0.5 else "🟡 High" if corr >= 0.3 else "🟢 Moderate"
        print(f"{rank:<6} {feature:<35} {corr:>15.4f} {impact:>15}")

# ========== Multicollinearity Analysis ==========
def multicollinearity_analysis(correlation_matrix):
    """Identify highly correlated features (multicollinearity)"""
    print("\n" + "="*70)
    print("🔗 MULTICOLLINEARITY ANALYSIS")
    print("="*70)
    
    # Find pairs of highly correlated features
    high_corr_pairs = []
    
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            corr_value = correlation_matrix.iloc[i, j]
            if abs(corr_value) > 0.8:  # High correlation threshold
                feature1 = correlation_matrix.columns[i]
                feature2 = correlation_matrix.columns[j]
                if feature1 != 'Target' and feature2 != 'Target':
                    high_corr_pairs.append((feature1, feature2, corr_value))
    
    if high_corr_pairs:
        print("\n⚠️  HIGHLY CORRELATED FEATURE PAIRS (|r| > 0.8):")
        print("-" * 70)
        for feat1, feat2, corr in sorted(high_corr_pairs, key=lambda x: abs(x[2]), reverse=True):
            print(f"  {feat1:<30} ↔ {feat2:<30} : {corr:+.4f}")
        print("\n💡 Consider removing one feature from each pair to reduce redundancy")
    else:
        print("\n✅ No severe multicollinearity detected (all |r| < 0.8)")

# ========== Visualization ==========
def create_visualizations(correlation_matrix, target_correlations, df):
    """Create correlation visualizations"""
    print("\n" + "="*70)
    print("📊 GENERATING VISUALIZATIONS")
    print("="*70)
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (16, 12)
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 12))
    
    # 1. Full Correlation Heatmap
    ax1 = plt.subplot(2, 2, 1)
    sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title('Full Correlation Matrix', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(fontsize=8)
    
    # 2. Target Correlations Bar Plot
    ax2 = plt.subplot(2, 2, 2)
    target_corr_sorted = target_correlations.drop('Target').sort_values()
    colors = ['red' if x > 0 else 'green' for x in target_corr_sorted]
    target_corr_sorted.plot(kind='barh', color=colors, ax=ax2)
    plt.title('Feature Correlations with Dropout Risk', fontsize=14, fontweight='bold')
    plt.xlabel('Correlation Coefficient', fontsize=12)
    plt.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    plt.grid(axis='x', alpha=0.3)
    
    # 3. Attendance Pattern Over Time
    ax3 = plt.subplot(2, 2, 3)
    weeks = [f'Week_{i}_Attendance' for i in range(1, 13)]
    available_weeks = [w for w in weeks if w in df.columns]
    
    if available_weeks:
        at_risk = df[df['Target'] == 1]
        not_at_risk = df[df['Target'] == 0]
        
        not_risk_avg = [not_at_risk[w].mean() for w in available_weeks]
        at_risk_avg = [at_risk[w].mean() for w in available_weeks]
        
        weeks_labels = [f'W{i}' for i in range(1, len(available_weeks)+1)]
        
        plt.plot(weeks_labels, not_risk_avg, marker='o', linewidth=2, 
                label='Not At Risk', color='green')
        plt.plot(weeks_labels, at_risk_avg, marker='s', linewidth=2, 
                label='At Risk', color='red')
        plt.title('Average Attendance Pattern (12 Weeks)', fontsize=14, fontweight='bold')
        plt.xlabel('Week', fontsize=12)
        plt.ylabel('Attendance (%)', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(alpha=0.3)
    
    # 4. Top Features Importance
    ax4 = plt.subplot(2, 2, 4)
    top_features = target_correlations.drop('Target').abs().sort_values(ascending=True).tail(10)
    colors_imp = ['red' if target_correlations[f] > 0 else 'green' for f in top_features.index]
    top_features.plot(kind='barh', color=colors_imp, ax=ax4)
    plt.title('Top 10 Most Important Features (by |correlation|)', fontsize=14, fontweight='bold')
    plt.xlabel('Absolute Correlation', fontsize=12)
    plt.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    output_file = 'correlation_analysis_results.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✅ Visualizations saved to: {output_file}")
    
    # Show plot
    plt.show()

# ========== Insights & Recommendations ==========
def generate_insights(target_correlations, df):
    """Generate actionable insights from correlation analysis"""
    print("\n" + "="*70)
    print("💡 KEY INSIGHTS & RECOMMENDATIONS")
    print("="*70)
    
    # Get top positive and negative correlations
    top_positive = target_correlations[target_correlations > 0].drop('Target').head(3)
    top_negative = target_correlations[target_correlations < 0].head(3)
    
    print("\n🔴 STRONGEST RISK INDICATORS (Positive Correlation):")
    for feature, corr in top_positive.items():
        print(f"  • {feature}: {corr:.4f}")
        if 'Decline' in feature:
            print(f"    → Students with higher decline scores are at greater risk")
        elif 'Lowest' in feature:
            print(f"    → Lower minimum attendance strongly predicts dropout risk")
    
    print("\n🟢 STRONGEST PROTECTIVE FACTORS (Negative Correlation):")
    for feature, corr in top_negative.items():
        print(f"  • {feature}: {corr:.4f}")
        if 'Average' in feature:
            print(f"    → Higher average attendance significantly reduces risk")
        elif 'Week' in feature:
            print(f"    → Consistent weekly attendance is protective")
        elif 'score' in feature.lower():
            print(f"    → Better academic performance reduces dropout risk")
    
    print("\n📋 ACTIONABLE RECOMMENDATIONS:")
    print("-" * 70)
    print("  1. Monitor Attendance Decline Score as primary early warning indicator")
    print("  2. Intervene when average attendance drops below 75%")
    print("  3. Pay special attention to students with declining weekly patterns")
    print("  4. Academic support can help reduce dropout risk")
    print("  5. Track recent weeks (11-12) more closely for immediate intervention")

# ========== Main Execution ==========
def main():
    print("\n" + "="*70)
    print("🎓 STUDENT DROPOUT PREDICTION - CORRELATION ANALYSIS")
    print("="*70)
    
    # Load data
    df = load_and_prepare_data()
    
    # Perform correlation analysis
    correlation_matrix, target_correlations = correlation_analysis(df)
    
    # Statistical analysis
    statistical_analysis(df)
    
    # Attendance pattern analysis
    attendance_pattern_analysis(df)
    
    # Feature importance
    feature_importance_analysis(correlation_matrix, target_correlations)
    
    # Multicollinearity check
    multicollinearity_analysis(correlation_matrix)
    
    # Generate insights
    generate_insights(target_correlations, df)
    
    # Create visualizations
    create_visualizations(correlation_matrix, target_correlations, df)
    
    print("\n" + "="*70)
    print("✅ CORRELATION ANALYSIS COMPLETE!")
    print("="*70)

if __name__ == "__main__":
    main()
