import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime

ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")

from streamlit_autorefresh import st_autorefresh

count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

if count == 0:
    st.write("Count is zero")
elif count % 3 == 0 and count % 5 == 0:
    st.write("FizzBuzz")
elif count % 3 == 0:
    st.write("Fizz")
elif count % 5 == 0:
    st.write("Buzz")
else:
    st.write(f"Count: {count}")

# Load the attendance CSV file
attendance_file = f"/Users/shuvamghosh/Desktop/Smart Attendance/Attendance/Attendance_{date}.csv"
if os.path.exists(attendance_file):
    df = pd.read_csv(attendance_file)
    st.dataframe(df.style.highlight_max(axis=0))
else:
    st.write("No attendance data available for today.")