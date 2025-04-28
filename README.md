# GymTracker

This project is a Streamlit-based web application that provides insights into gym attendance and member activity trends. It allows users to manage gym attendance records and visualize trends through interactive charts.

The app is integrated with a local SQLite database to fetch and manipulate data, allowing users to view visualizations, add new attendance records, delete existing entries, and update gym activity data interactively.

Synthetic data was used, which was generated programmatically to simulate realistic gym member behavior.

---

## Features

### 📊 Home Page (Attendance Insights)
- **Attendance Trend Line Chart:** Visualizes daily check-ins over a selected date range.
- **Class Participation Bar Chart:** Displays participation across different gym classes.
- **Equipment Usage Pie Chart:** Shows distribution of equipment usage among members.

---

### 📝 Manage Gym Records Page
- **Add New Record:** Insert new gym attendance entries into the database.
- **Fetch Records:** Retrieve records within a specified date range.
- **Update Record:** Modify existing gym entries (class attended, equipment used, etc.)
- **Delete Record:** Remove gym records based on check-in timestamp.

---

## Screenshots

### Home Page

> *Attendance Insights with Trend Line Chart, Class Participation, and Equipment Usage*

![image](https://github.com/user-attachments/assets/34e59792-0faa-4407-9676-153867560dd1)

**Figure 1:** Attendance Trend Line Chart showing number of daily gym check-ins.

![image](https://github.com/user-attachments/assets/26a9b13f-ff29-4f53-b351-9308d2645c0e)

**Figure 2:** Bar Chart of class participation and Pie Chart showing equipment usage distribution.

---

### Manage Gym Records Page

> *Manage attendance records — Add, Fetch, Update, Delete*

![image](https://github.com/user-attachments/assets/18b1ad53-10b6-4a46-8b42-ef509359ae2f)

**Figure 3:** Manage Gym Records page where users can add new attendance records.

![image](https://github.com/user-attachments/assets/8f1ccaca-9895-444b-81ad-c3b5365696ff)

![image](https://github.com/user-attachments/assets/517042ba-0269-4826-9f1b-954ba34c26b4)

**Figure 4:** Fetch, update, and delete existing records based on check-in timestamp.

---

## Setup Instructions

### 📥 Installation

1. Clone or download this repository.
2. Install required Python packages:

pip install -r requirements.txt


### 🚀 Run the Application

From the project directory, run the following command:

streamlit run main.py

The application will launch at:

http://localhost:8501

---

## Future Enhancements

1) Introduce user authentication to restrict access to authorized staff or gym managers.

2) Add more detailed visualizations, such as attendance heatmaps and peak hour analysis, for deeper operational insights.

3) Migrate from SQLite to a cloud-hosted database (e.g., PostgreSQL) for better scalability and remote access.

4) Optimize database queries and implement pagination for smoother handling of larger datasets.
