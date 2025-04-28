

import sqlite3
import random
from datetime import datetime, timedelta

# Connect to SQLite database
conn = sqlite3.connect('gym_tracker.db')
cursor = conn.cursor()

# Define sample values
first_names = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah", "Ivan", "Julia", "Kevin", "Laura", "Mike", "Nina", "Oscar", "Paula", "Quincy", "Rachel", "Steve", "Tina", "Umar", "Victor", "Wendy", "Xavier", "Yara", "Zane"]
last_names = ["Smith", "Johnson", "Brown", "Taylor", "Anderson", "Clark", "Lewis", "Walker", "Young", "Hall"]

membership_status_choices = ["Active", "Expired"]
class_choices = ["Yoga", "HIIT", "Zumba", "Football", "Pilates", "CrossFit", "Spinning", "Kickboxing", "Swimming", "None"]
equipment_choices = ["Treadmill", "Dumbbells", "Resistance Bands", "Rowing Machine", "Elliptical", "Stationary Bike", "Kettlebell", "Pull-up Bar", "Battle Ropes", "Medicine Ball"]
attendance_freq_choices = ["High", "Medium", "Low"]

# Generate random records
def generate_random_record():
    member_name = random.choice(first_names) + " " + random.choice(last_names)
    membership_status = random.choice(membership_status_choices)

    # Random timestamp within last 6 months
    start_date = datetime(2024, 11, 1)
    random_days = random.randint(0, 180)
    random_minutes = random.randint(5, 60 * 18)  # random time during the day
    check_in_timestamp = start_date + timedelta(days=random_days, minutes=random_minutes)

    # Randomly assign class or None
    class_attended = random.choice(class_choices)
    if class_attended == "None":
        class_attended = None

    # 1 to 4 equipment used randomly
    used_equipments = random.sample(equipment_choices, random.randint(1, 4))
    equipment_used = ", ".join(used_equipments)

    usage_duration = random.randint(15, 120)  # minutes spent in gym
    attendance_freq = random.choice(attendance_freq_choices)

    return (member_name, membership_status, check_in_timestamp, class_attended, equipment_used, usage_duration, attendance_freq)

# Insert 1000 records
records = [generate_random_record() for _ in range(1000)]

cursor.executemany('''
INSERT INTO GymRecords (member_name, membership_status, check_in_timestamp, class_attended, equipment_used, usage_duration, attendance_freq)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', records)

conn.commit()
conn.close()

print("✅ Successfully inserted 1000 diverse gym records into gym_tracker.db!")
