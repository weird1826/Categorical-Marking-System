import random
from datetime import datetime, timedelta
import names  # pip install names

def generate_test_data(num_records=1000):
    # Generate dates between 1990 and 2005
    start_date = datetime(1990, 1, 1)
    end_date = datetime(2005, 12, 31)
    
    with open('test_data.txt', 'w') as f:
        for i in range(num_records):
            # Generate random student ID (2 digits, zero-padded)
            student_id = f"{i:02d}"
            
            # Generate random name
            name = names.get_full_name()
            
            # Generate random date of birth
            days_between = (end_date - start_date).days
            random_days = random.randint(0, days_between)
            random_date = start_date + timedelta(days=random_days)
            dob = random_date.strftime('%Y-%m-%d')
            
            # Generate 4 random scores
            scores = [random.uniform(0, 100) for _ in range(4)]
            scores_str = ','.join(f"{score:.2f}" for score in scores)
            
            # Write to file in required format
            f.write(f"{student_id},{name},{dob},{scores_str}\n")

if __name__ == "__main__":
    generate_test_data()
    print("Test data generated in test_data.txt")