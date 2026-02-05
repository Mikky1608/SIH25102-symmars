import pandas as pd
import re

def generate_email(student_name, student_id, institute_id):
    """Generate a realistic email address from student name and ID"""
    # Clean the name - remove extra spaces and convert to lowercase
    name = student_name.strip().lower()
    
    # Split name into parts
    name_parts = name.split()
    
    if len(name_parts) >= 2:
        first_name = name_parts[0]
        last_name = name_parts[-1]
        
        # Create email variations
        email_formats = [
            f"{first_name}.{last_name}",
            f"{first_name}{last_name}",
            f"{first_name}.{last_name}{str(student_id)[-2:]}",
            f"{first_name[0]}{last_name}",
            f"{first_name}.{last_name[0]}"
        ]
        
        # Choose format based on student_id for variety
        format_index = student_id % len(email_formats)
        username = email_formats[format_index]
    else:
        # Single name case
        username = f"{name}{str(student_id)[-2:]}"
    
    # Remove any special characters
    username = re.sub(r'[^a-z0-9.]', '', username)
    
    # Use Gmail domain
    domain = "gmail.com"
    
    return f"{username}@{domain}"

def add_email_to_datasets():
    """Add email column to all sample datasets"""
    
    datasets = [
        ("sample_student_dataset.csv", "Sample Student Dataset (100 students)"),
        ("sample_batch_students.csv", "Sample Batch Dataset (10 students)"),
        ("comprehensive_student_dataset.csv", "Comprehensive Dataset (4000 students)")
    ]
    
    for filename, description in datasets:
        try:
            print(f"\n📧 Processing {description}...")
            
            # Load dataset
            df = pd.read_csv(filename)
            print(f"   Loaded: {len(df)} students")
            
            # Generate emails
            df['student_email'] = df.apply(
                lambda row: generate_email(
                    row['student_name'], 
                    row['student_id'], 
                    row['institute_id']
                ), axis=1
            )
            
            # Reorder columns to put email after student_name
            cols = df.columns.tolist()
            if 'student_email' in cols:
                cols.remove('student_email')
                # Insert after student_name
                name_index = cols.index('student_name')
                cols.insert(name_index + 1, 'student_email')
                df = df[cols]
            
            # Save updated dataset
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"   ✅ Updated {filename} with email addresses")
            
            # Show sample emails
            print(f"   📧 Sample emails:")
            sample_emails = df[['student_name', 'student_email']].head(5)
            for _, row in sample_emails.iterrows():
                print(f"      {row['student_name']} → {row['student_email']}")
                
        except FileNotFoundError:
            print(f"   ⚠️  File {filename} not found, skipping...")
        except Exception as e:
            print(f"   ❌ Error processing {filename}: {e}")

def main():
    print("📧 ADDING EMAIL ADDRESSES TO STUDENT DATASETS")
    print("=" * 60)
    
    add_email_to_datasets()
    
    print(f"\n✅ Email addresses added to all available datasets!")
    print("\n📋 Email Format Examples:")
    print("   • firstname.lastname@gmail.com")
    print("   • firstnamelastname@gmail.com")
    print("   • firstname.lastname01@gmail.com")
    print("   • f.lastname@gmail.com")
    
    print(f"\n🎯 Updated Datasets:")
    print("   • sample_student_dataset.csv (100 students)")
    print("   • sample_batch_students.csv (10 students)")
    print("   • comprehensive_student_dataset.csv (4000 students)")

if __name__ == "__main__":
    main()