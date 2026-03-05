"""
Add university email addresses to all student datasets
Format: firstname.lastname.studentid@university.edu
"""

import pandas as pd
import os

def generate_university_email(student_name, student_id, domain="university.edu"):
    """Generate university email address"""
    # Clean and format name
    name_parts = str(student_name).lower().strip().split()
    
    if len(name_parts) >= 2:
        email_prefix = f"{name_parts[0]}.{name_parts[-1]}.{student_id}"
    else:
        email_prefix = f"{name_parts[0]}.{student_id}" if name_parts else f"student.{student_id}"
    
    # Remove special characters
    email_prefix = ''.join(c for c in email_prefix if c.isalnum() or c == '.')
    
    return f"{email_prefix}@{domain}"

def add_emails_to_dataset(input_file, output_file=None):
    """Add university emails to a dataset"""
    print(f"\n📧 Processing: {input_file}")
    
    # Read dataset
    df = pd.read_csv(input_file)
    print(f"   Loaded {len(df)} records")
    
    # Check if student_name and student_id columns exist
    if 'student_name' not in df.columns or 'student_id' not in df.columns:
        print(f"   ⚠️  Skipping - missing required columns")
        return
    
    # Generate university emails
    df['university_email'] = df.apply(
        lambda row: generate_university_email(row['student_name'], row['student_id']),
        axis=1
    )
    
    # Save updated dataset
    if output_file is None:
        output_file = input_file
    
    df.to_csv(output_file, index=False)
    print(f"   ✅ Added university emails")
    print(f"   📧 Sample: {df['university_email'].iloc[0]}")
    
    return df

def main():
    """Add university emails to all datasets"""
    print("="*70)
    print("🎓 ADDING UNIVERSITY EMAILS TO ALL DATASETS")
    print("="*70)
    
    # List of datasets to update
    datasets = [
        'comprehensive_student_dataset.csv',
        'sample_student_dataset.csv',
        'sample_batch_students.csv'
    ]
    
    for dataset in datasets:
        if os.path.exists(dataset):
            add_emails_to_dataset(dataset)
        else:
            print(f"\n⚠️  File not found: {dataset}")
    
    # Also update institute datasets if they exist
    print("\n" + "="*70)
    print("📊 UPDATING INSTITUTE DATASETS")
    print("="*70)
    
    institute_files = [
        'ml/data/Students_Institute1.csv',
        'ml/data/Students_Institute2.csv'
    ]
    
    for file in institute_files:
        if os.path.exists(file):
            add_emails_to_dataset(file)
    
    print("\n" + "="*70)
    print("✅ ALL DATASETS UPDATED WITH UNIVERSITY EMAILS!")
    print("="*70)
    print("\n📧 Email Format: firstname.lastname.studentid@university.edu")
    print("👨‍💼 Admin Email: admin@university.edu")
    print("\n💡 You can now use the API-based email service to send notifications!")

if __name__ == "__main__":
    main()
