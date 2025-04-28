# main.py

# Import libraries
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import date, datetime

# Set wide page layout
st.set_page_config(layout="wide")

# Connect to SQLite
conn = sqlite3.connect('gym_tracker.db', check_same_thread=False)
cursor = conn.cursor()

# Function to fetch data
def fetch_data(start_date, end_date):
    try:
        query = f"""
            SELECT * FROM GymRecords
            WHERE DATE(check_in_timestamp) BETWEEN '{start_date}' AND '{end_date}'
        """
        df = pd.read_sql_query(query, conn)
        st.dataframe(df, use_container_width=True)
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to plot attendance trend (Line Chart)
def plot_attendance_trend(start_date, end_date):
    try:
        df = fetch_data(start_date, end_date)
        df["check_in_date"] = pd.to_datetime(df["check_in_timestamp"]).dt.date
        if not df.empty:
            trend = df.groupby("check_in_date").size().reset_index(name="Check-Ins")
            st.line_chart(trend.set_index("check_in_date")["Check-Ins"])
        else:
            st.info("No data available for selected date range.")

    except Exception as e:
        st.error(f"Error plotting line chart: {e}")

# Function to plot class participation (Bar Chart) with date filter
def plot_class_participation(start_date, end_date):
    try:
        query = f"""
            SELECT class_attended FROM GymRecords
            WHERE DATE(check_in_timestamp) BETWEEN '{start_date}' AND '{end_date}'
              AND class_attended IS NOT NULL
        """
        df = pd.read_sql_query(query, conn)
        if not df.empty:
            class_counts = df["class_attended"].value_counts().reset_index()
            class_counts.columns = ["Class", "Participants"]
            st.bar_chart(class_counts.set_index("Class"))
        else:
            st.info("No class participation data available for selected date range.")
    except Exception as e:
        st.error(f"Error plotting bar chart: {e}")


# Function to plot equipment usage (Pie Chart) with date filter
def plot_equipment_usage(start_date, end_date):
    try:
        query = f"""
            SELECT equipment_used FROM GymRecords
            WHERE DATE(check_in_timestamp) BETWEEN '{start_date}' AND '{end_date}'
              AND equipment_used IS NOT NULL
        """
        df = pd.read_sql_query(query, conn)
        if not df.empty:
            exploded = df["equipment_used"].str.split(", ").explode().value_counts().reset_index()
            exploded.columns = ["Equipment", "Usage Count"]
            fig = px.pie(exploded, names="Equipment", values="Usage Count")
            fig.update_layout(width=400, height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No equipment usage data available for selected date range.")
    except Exception as e:
        st.error(f"Error plotting pie chart: {e}")


# Home Page
def home_page():
    st.header(":blue[GYM ATTENDANCE INSIGHTS]", divider='blue')

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", date(2025, 4, 1))
    with col2:
        end_date = st.date_input("End Date", date(2025, 4, 30))

    if start_date > end_date:
        st.error("Start date cannot be after end date.")
    else:
        st.subheader("Attendance Trend")
        plot_attendance_trend(start_date, end_date)

        st.markdown("---")
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Class Participation")
            plot_class_participation(start_date, end_date)
        with col4:
            st.subheader("Equipment Usage")
            plot_equipment_usage(start_date, end_date)

# Record Manipulation Page
def record_manipulation():
    st.header("Manage Gym Records")

    st.subheader("➤ Add New Record")
    col1, col2 = st.columns(2)
    member_name = col1.text_input("Member Name")
    membership_status = col2.selectbox("Membership Status", ["Active", "Expired"])
    check_in_date = col1.date_input("Check-in Date", date.today())
    check_in_time = col2.time_input("Check-in Time")
    class_attended = col1.text_input("Class Attended (Optional)")
    equipment_used = col2.text_input("Equipment Used (comma-separated)")
    usage_duration = col1.number_input("Usage Duration (minutes)", min_value=0)
    attendance_freq = col2.selectbox("Attendance Frequency", ["High", "Medium", "Low"])

    if st.button("Add Record"):
        try:
            timestamp = datetime.combine(check_in_date, check_in_time)
            cursor.execute("""
                INSERT INTO GymRecords (member_name, membership_status, check_in_timestamp, class_attended, equipment_used, usage_duration, attendance_freq)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (member_name, membership_status, timestamp, class_attended, equipment_used, usage_duration, attendance_freq))
            conn.commit()
            st.success("Record added successfully!")
        except Exception as e:
            st.error(f"Error adding record: {e}")

    st.markdown("---")
    st.subheader("➤ Fetch Records")
    col3, col4 = st.columns(2)
    start_date = col3.date_input("Start Date", date(2025, 4, 1), key="fetch_start")
    end_date = col4.date_input("End Date", date(2025, 4, 30), key="fetch_end")

    if st.button("Fetch Records"):
        fetch_data(start_date, end_date)

    st.markdown("---")
    st.subheader("➤ Delete a Record")

    # Input for date and time of record to delete
    del_check_in_date = st.date_input("Check-in Date to Delete", key="del_date")
    del_check_in_time = st.time_input("Check-in Time to Delete", key="del_time")

    if st.button("Delete Record"):
        try:
            timestamp_to_delete = datetime.combine(del_check_in_date, del_check_in_time)

            cursor.execute("""
                DELETE FROM GymRecords
                WHERE check_in_timestamp = ?
            """, (timestamp_to_delete,))
            conn.commit()

            if cursor.rowcount > 0:
                st.success("Record deleted successfully!")
            else:
                st.warning("No matching record found to delete.")
        except Exception as e:
            st.error(f"Error deleting record: {e}")


    st.markdown("---")
    st.subheader("➤ Update a Record")

    # Inputs to find the record to update
    upd_check_in_date = st.date_input("Check-in Date to Update", key="upd_date")
    upd_check_in_time = st.time_input("Check-in Time to Update", key="upd_time")

    # New updated values
    new_class_attended = st.text_input("New Class Attended (Optional)", key="upd_class")
    new_equipment_used = st.text_input("New Equipment Used (comma-separated)", key="upd_equipment")
    new_usage_duration = st.number_input("New Usage Duration (minutes)", min_value=0, key="upd_duration")
    new_attendance_freq = st.selectbox("New Attendance Frequency", ["High", "Medium", "Low"], key="upd_freq")

    if st.button("Update Record"):
        try:
            timestamp_to_update = datetime.combine(upd_check_in_date, upd_check_in_time)

            cursor.execute("""
                UPDATE GymRecords
                SET class_attended = ?, equipment_used = ?, usage_duration = ?, attendance_freq = ?
                WHERE check_in_timestamp = ?
            """, (new_class_attended, new_equipment_used, new_usage_duration, new_attendance_freq, timestamp_to_update))
            conn.commit()

            if cursor.rowcount > 0:
                st.success("Record updated successfully!")
            else:
                st.warning("No matching record found to update.")
        except Exception as e:
            st.error(f"Error updating record: {e}")


# Sidebar Navigation
page = st.sidebar.radio("Navigation", ["Home", "Manage Records"])

if page == "Home":
    home_page()
elif page == "Manage Records":
    record_manipulation()
