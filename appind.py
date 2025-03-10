# STEP 1: Importing libraries
import streamlit as st  # Used to create the web app
import seaborn as sns  # Used to load datasets and create visualizations
import pandas as pd
import random  # Used to randomly select the chart
import time  # Used to measure time taken by users to respond
import matplotlib.pyplot as plt
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- GOOGLE SHEET IMPLEMENTATION ---

# Configure credentials
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from Streamlit Secrets
credentials_dict = st.secrets["gcp_service_account"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, SCOPE)

# Authenticate with Google Sheets
client = gspread.authorize(credentials)

# Open the Google Sheet
SHEET_URL = "https://docs.google.com/spreadsheets/d/1g8ZUEXEzzHFaBfoOhFe6x-0bJvGhy_1-mZcuyv65uzU/edit?usp=sharing"
spreadsheet = client.open_by_url(SHEET_URL)
worksheet = spreadsheet.sheet1  # Select the first worksheet

# Function to load data from Google Sheets
def load_data():
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    st.write("✅ Successfully loaded data from Google Sheets!")  # Debugging
    st.write(df.head())  # Show first rows to verify loading
    return df

# Load data from Google Sheets into a DataFrame
df = load_data()

# --- BUSINESS QUESTION ---
st.title("A/B Testing Experiment - Taxi Data")
st.write("### Business Question: Which day of the week records more taxi rides?")

# Convert the date column and extract the day of the week
df["pickup"] = pd.to_datetime(df["pickup"])
df["day_of_week"] = df["pickup"].dt.day_name()

# --- CREATE CHARTS ---
# Function for Chart A (Bar Chart)
def plot_chart_a():
    fig, ax = plt.subplots()
    sns.countplot(x=df["day_of_week"], order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], ax=ax)
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel("Number of Rides")
    ax.set_title("Number of Rides per Day (Bar Chart)")
    st.pyplot(fig)

# Function for Chart B (Line Chart)
def plot_chart_b():
    fig, ax = plt.subplots()
    df.groupby("day_of_week").size().reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]).plot(kind="line", marker="o", ax=ax)
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel("Number of Rides")
    ax.set_title("Number of Rides per Day (Line Chart)")
    st.pyplot(fig)

# --- CREATE APP TABS ---
tab1, tab2 = st.tabs(["Home", "About"])

with tab1:
    st.header("Experiment: Compare Two Charts")

    # Session state variables
    if "chart_selected" not in st.session_state:
        st.session_state.chart_selected = None

    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    # Button to show a random chart
    if st.button("Show Chart"):
        st.session_state.chart_selected = random.choice(["A", "B"])
        st.session_state.start_time = time.time()  # Start timer

    # Display the randomly selected chart
    if st.session_state.chart_selected == "A":
        plot_chart_a()
    elif st.session_state.chart_selected == "B":
        plot_chart_b()

    # Button to measure response time
    if st.session_state.chart_selected:
        if st.button("I answered the question"):
            end_time = time.time()
            elapsed_time = end_time - st.session_state.start_time
            st.write(f"You took {elapsed_time:.2f} seconds to answer.")

with tab2:  # About tab
    st.header("About this App")
    st.write("This app compares two different visualizations to determine which one is more effective in analyzing taxi demand during a week.")
