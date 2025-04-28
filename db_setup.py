
# Import necessary libraries
import sqlite3
import random
from datetime import datetime, timedelta

# Connect to SQLite database (creates gym_tracker.db if it doesn't exist)
conn = sqlite3.connect('gym_tracker.db')
cursor = conn.cursor()

# ==================== TABLE CREATION ====================
cursor.execute('''
CREATE TABLE IF NOT EXISTS GymRecords (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_name TEXT NOT NULL,
    membership_status TEXT NOT NULL CHECK (membership_status IN ('Active', 'Expired')),
    check_in_timestamp DATETIME NOT NULL,
    class_attended TEXT,
    equipment_used TEXT,
    usage_duration INTEGER NOT NULL CHECK (usage_duration >= 0),
    attendance_freq TEXT NOT NULL CHECK (attendance_freq IN ('High', 'Medium', 'Low'))
)
''')
conn.commit()

# ==================== SAMPLE DATA GENERATION ====================
# Done by: [Your Name]

# Sample lists for random value generation
first_names = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah", "Ivan", "Julia", "Kevin", "Laura", "Mike", "Nina", "Oscar", "Paula", "Quincy", "Rachel", "Steve", "Tina", "Umar", "Victor", "Wendy", "Xavier", "Yara", "Zane"]
last_names = ["Smith", "Johnson", "Brown", "Taylor", "Anderson", "Clark", "Lewis", "Walker", "Young", "Hall"]
membership_status_choices = ["Active", "Expired"]
class_choices = ["Yoga", "HIIT", "Zumba", "Football", "Pilates", "CrossFit", "Spinning", "Kickboxing", "Swimming", "None"]
equipment_choices = ["Treadmill", "Dumbbells", "Resistance Bands", "Rowing Machine", "Elliptical", "Stationary Bike", "Kettlebell", "Pull-up Bar", "Battle Ropes", "Medicine Ball"]
attendance_freq_choices = ["High", "Medium", "Low"]

# Function to generate one random gym record
def generate_random_record():
    member_name = random.choice(first_names) + " " + random.choice(last_names)
    membership_status = random.choice(membership_status_choices)

    # Random timestamp within the last 6 months
    start_date = datetime(2024, 11, 1)
    random_days = random.randint(0, 180)
    random_minutes = random.randint(5, 60 * 18)  # Random time during the day
    check_in_timestamp = start_date + timedelta(days=random_days, minutes=random_minutes)

    # Randomly assign class or None
    class_attended = random.choice(class_choices)
    if class_attended == "None":
        class_attended = None

    # 1 to 4 equipments used randomly
    used_equipments = random.sample(equipment_choices, random.randint(1, 4))
    equipment_used = ", ".join(used_equipments)

    usage_duration = random.randint(15, 120)  # minutes spent in gym
    attendance_freq = random.choice(attendance_freq_choices)

    return (member_name, membership_status, check_in_timestamp, class_attended, equipment_used, usage_duration, attendance_freq)

# Generate 1000 random records
records = [generate_random_record() for _ in range(1000)]

# Insert generated records into the database
cursor.executemany('''
INSERT INTO GymRecords (member_name, membership_status, check_in_timestamp, class_attended, equipment_used, usage_duration, attendance_freq)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', records)

conn.commit()
conn.close()

print("✅ Successfully created table and inserted 1000 diverse gym records into gym_tracker.db!")
