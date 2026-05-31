"""
Hello and welcome to my minimalist time tracker.

This project is a simple, forward-counting time tracker that behaves like a stopwatch. 
The core objective was to implement the following essential features:

- Start time tracking
- Stop time tracking
- Calculate elapsed time
- Export recorded time entries as a CSV file for use in Excel or similar tools

The focus of the project is on simplicity, elegance and learning.
Thank you for taking the time to go through my program and remember to go through the attached Readme file!

"""

# ----------------------------------------- Import Libraries ----------------------------------------- #

import streamlit as st
from datetime import datetime
import pandas as pd

# ----------------------------------------- Start Session ----------------------------------------- #

st.set_page_config(layout="wide", page_title="Productivity Tracker") # Setting page width

if "start_datetime" not in st.session_state:
    st.session_state.start_datetime = None
    
if "elapsed_datetime" not in st.session_state:
    st.session_state.elapsed_datetime = None
    
# List to store things in memory
if "history" not in st.session_state:
    st.session_state.history = []

# ----------------------------------------- Functions ----------------------------------------- #

# Start time function
def start_timer():
    st.session_state.start_datetime = datetime.now().replace(microsecond=0)
    st.session_state.elapsed_datetime = None
    

# End time function
    # Using end timer function to calculate elapsed time
def end_timer():
    end_datetime = datetime.now().replace(microsecond=0)
    elapsed_datetime = end_datetime - st.session_state.start_datetime       
    
    st.session_state.elapsed_datetime = elapsed_datetime

    # Dictionary for new entry
    new_entry = {
        "Start": st.session_state.start_datetime,
        "End": end_datetime,
        "Elapsed": elapsed_datetime
    }
    # Append new entry to the table
    st.session_state.history.append(new_entry)

    # Need to reset prev button - otherwise there will a error saying timer is still running
    st.session_state.start_datetime = None

# ----------------------------------------- UI and Interaction ----------------------------------------- #

st.title("Minimalist Productivity Tracker")

# Start button
    # if statements included inside for error handling - Warning to user on wrong input

if st.button("Start timer"):
    if st.session_state.start_datetime is not None:
         st.warning("Timer is already running")
    else:
        start_timer()

# End button
    # if statements included inside for error handling - Warning to user on wrong input

if st.button("End timer"):
    if st.session_state.start_datetime is None:
        st.warning("Please start the timer first")
    else:
        end_timer()
        st.success(f"Time recorded! Elapsed: {st.session_state.elapsed_datetime}")

# Displaying the current status
st.subheader("Current tracker status")
st.write("Start Time:", st.session_state.start_datetime)
st.write("Elapsed Time:", st.session_state.elapsed_datetime)

# ----------------------------------------- Display History and Export as CSV ----------------------------------------- #

if len(st.session_state.history) > 0:
    
    st.subheader("Time Entry History")
    
    # Convert the history list (the "Memory") into a DataFrame
    history_df = pd.DataFrame(st.session_state.history)
    
    # Display the table visually in the app
    st.dataframe(history_df)

    # Prepare for CSV export
    csv_output = history_df.to_csv(index=False).encode('utf-8')

    # Export button
    st.download_button(
        label="Export Full History as CSV",
        data=csv_output,
        file_name="time_sheet_history.csv",
        mime="text/csv"
    )
