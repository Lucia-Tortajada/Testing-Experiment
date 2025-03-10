#STEP 1: Importing libraries
import streamlit as st #used to create the web app
import seaborn as sns #used to load datasets and create visualizations
import pandas as pd
import random #used to randomly select  the chart 
import time #used to measure time taken by users to respond
import matplotlib.pyplot as plt



#Business Question : Which day of teh week records more taxi rides ? -> will help us understand demand distribution along the week

#STEP 2: Loading and processing the taxis dataset
# Load the taxis dataset
df = sns.load_dataset("taxis")

# Convert the date column and extract the day of the week
df["pickup"] = pd.to_datetime(df["pickup"])
df["day_of_week"] = df["pickup"].dt.day_name()

#STEP 3: App title and Business Question

st.title("A/B Testing Experiment - Taxi Data")
st.write("### Business Question: Which day of the week records more taxi rides?")

#STEP 4:Creating two chart funtions

# Function for Chart A (Bar Chart): Creates a bar chart to show the number of taxi rides per day
def plot_chart_a():
    fig, ax = plt.subplots()
    sns.countplot(x=df["day_of_week"], order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], ax=ax)
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel("Number of Rides")
    ax.set_title("Number of Rides per Day (Bar Chart)")
    st.pyplot(fig)

# Function for Chart B (Line Chart) : Creates a Line chart showing the num of rides per day 
def plot_chart_b():
    fig, ax = plt.subplots()
    df.groupby("day_of_week").size().reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]).plot(kind="line", marker="o", ax=ax)
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel("Number of Rides")
    ax.set_title("Number of Rides per Day (Line Chart)")
    st.pyplot(fig)

#STEP 5: Create tabs to navigate inside the app ( Home: runs the experiment, About: explains the app)
# Create app tabs
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

with tab2: #About tab
    st.header("About this App")
    st.write("This app compares two different visualizations to determine which one is more effective in analyzing taxi demand during a week.")