"""
`streamlit run scripts/data/visualize.py` in console to start it up
"""

import pandas as pd
import streamlit as st

st.title("Titanic Dataset Explorer 🚢")

# Load the Titanic dataset
data = pd.read_csv("data/titanic.csv")

# Display basic information
st.write(f"**Total passengers:** {len(data)}")
st.write(f"**Survivors:** {data['Survived'].sum()} ({data['Survived'].mean() * 100:.1f}%)")

# Display the dataframe
st.dataframe(data)
