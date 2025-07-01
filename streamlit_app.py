import streamlit as st
import pandas as pd

# Configure page for mobile-friendly layout
st.set_page_config(
    page_title="Filiaalnummer Lookup",
    layout="centered",
    initial_sidebar_state="auto"
)

# Load data from the provided Excel file
@st.cache_data
def load_data():
    try:
        # For .xlsx files, use openpyxl engine
        df = pd.read_excel('klantenlijst.xlsx', engine='openpyxl')
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()
    return df

# Cache the data
df = load_data()

# App title
st.title("Filiaalnummer Lookup App")

# Input field for the filiaalnummer
fil_num = st.text_input("Enter filiaalnummer:")

# When the user enters a value, filter and display the matching rows
if fil_num:
    try:
        fil_num_val = int(fil_num)
    except ValueError:
        st.error("Please enter a valid integer for filiaalnummer.")
    else:
        result = df[df['filiaalnummer'] == fil_num_val]
        if not result.empty:
            st.dataframe(result)
        else:
            st.warning(f"No records found for filiaalnummer {fil_num_val}.")

# Instructions for running the app
st.markdown("---")
st.markdown(
    "**How to run:**\n"
    "1. Convert `klantenlijst.xls` to `klantenlijst.xlsx` in Excel.\n"
    "2. Ensure `klantenlijst.xlsx` is in the same directory as this script.\n"
    "3. Install dependencies: `pip install streamlit pandas openpyxl`\n"
    "4. Run the app with: `streamlit run streamlit_app.py`"
)
