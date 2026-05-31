
# Project Documentation: Minimalist Time Tracker

## Overview
The Minimalist Time Tracker is a web-based productivity tool designed to help users log their tasks in real-time. 
Built with the Streamlit framework, it provides a "stopwatch" experience where users can start a session, end it, and automatically log the duration into a downloadable file.

## Key Features
**Live Session Tracking:** Captures precise start and end times.

**State Persistence:** Uses session_state to ensure data isn't lost when the app reruns.

**Automated Calculations:** Automatically determines the time delta (elapsed time).

**Data Export:** Converts session history into a CSV file compatible with Excel and Google Sheets.

**Error Handling:** Prevents duplicate starts or ending a timer that hasn't begun.

**User Interface Flow**
- **Start:** User clicks "Start timer." The system records the current timestamp.

- **End:** User clicks "End timer." The system calculates the difference and saves the record.

- **View:** A dynamic table updates with every new entry.

- **Export:** User downloads the full log for external reporting.

## How to Run the program
- [Hosted on Streamlit - Linked to Github] https://minimalist-time-tracker.streamlit.app/
- [OR - On windows cmd prompt]  
  - **python --version** - check python version
  - **python -m pip install streamlit pandas** - Install streamlit and Pandas
  - **cd {file_path}** - Change directory to correct file you have downloaded the file
  - **python -m streamlit run app.py** - It should start



## Detailed description of code
This section is a description of the code used for the application

### Step 1 - Import Necessary Libraries

First, we import our necessary libraries 
 - **Streamlit (st)** -> The star of this project, Streamlit powers the web interface and state management.
  - **Datetime (datetime, timedelta)** -> Manages precise time calculations and formatting
 - **Pandas (pd)** -> Handles data organization and CSV conversion

### Step 2 - State Management

This critical code block establishes the application environment and initializes Streamlit Session State. As Streamlit scripts rerun from top to bottom with every user interaction, the app utilizes **st.session_state** to prevent data loss and be the program's memory

- **start_datetime, elapsed_datetime, history** -> Creating variables to act as the system's memory

### Step 3 - Defining Functions

Writing the logic and process that happens when a button is clicked
 - **def start_timer():** -> Capturing current datetime, omitting microseconds to achieve a cleaner look
 - **def end_timer():** -> Capturing the time the button is clicked and using it to calculate **elapsed_datetime** by subtracting start time from end time
 #### Create Dictionary
 - Assign **start_datetime, end_datetime, elapsed_datetime** to a new variable **new_entry**
#### Append new entry
 - **history.append(new_entry)** -> Append new entry to list - without this our program will only be able to export one Excel row at a time
#### Start state reset
- Setting start time back to **None** - otherwise we the Start button will not work for consecutive entries

### Step 4 - UI and Interaction

This section is where the UI design happens and how the input buttons for user input are designed
- **st.title("")** -> Used to display the application's title
- **st.button("Start button"):** -> Start button command wrapped in an if statement to handle improper use gracefully
- **st.button("End button"):** -> End buttom command wrapped in an if statement to handle improper use gracefully
  - if the command is successful (the end button was pressed after the start button) streamlit displays a success message using **st.success** and displays the **elapsed_datetime**
#### Display current status
- **st.subheader(), st.write("Start Time:"), st.write("Elapsed Time:")** -> Text that display the current state of the application

### Step 5 -Display History and Export as CSV

- Section responsible for **displaying all previously recorded time entries** stored in memory and presenting them in a readable table within the Streamlit interface
- The user is able to **export the full history of time entries** as a CSV file for use in Excel or similar tools
- **if len() > 0:** -> To check whether at least one time entry exists in memory, if the list is empty, nothing is displayed and no export option is shown
- **st.subheader()** -> Adds a visual section header in the Streamlit interface to clearly separate the history table from other UI elements
- **pd.DataFrame(st.session_state.history)** -> converts list to Pandas dataframe
- **st.dataframe(...)** -> Used to display the dataframe in the app visually
- **history_df.to_csv(index=False).encode('utf-8')** -> Prepares the data for export, removes index, output in utf-8 format for wide compatibility
- **st.download_button(...)** -> Exports current entries stored when clicked

## Limitations of the app

- Data is stored in memory, refreshing the browser or restarting the app clears the history

## Acknowledgements

- [Syntax reference] https://docs.streamlit.io/develop/quick-reference/cheat-sheet

- [Streamlit buttons] https://docs.streamlit.io/develop/concepts/design/buttons

- [Session state] https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state

- ChatGPT helped with figuring out parts of the syntax - particularly with regard to how to manage streamlit session and export as csv




