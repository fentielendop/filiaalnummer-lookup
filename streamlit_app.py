import streamlit as st
import pandas as pd

# Configure page for mobile-friendly layout
st.set_page_config(
    page_title="Filiaalnummer App",
    layout="centered",
    initial_sidebar_state="auto"
)

# Load data from the provided Excel file
def load_data():
    try:
        df = pd.read_excel('klantenlijst.xlsx', engine='openpyxl')
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    # Normalize column names
    original_cols = df.columns.tolist()
    normalized_cols = [col.strip().lower().replace(' ', '_') for col in original_cols]
    df.columns = normalized_cols
    col_mapping = dict(zip(original_cols, normalized_cols))
    return df, col_mapping

# Cache the data and get mapping
df, col_mapping = st.cache_data(load_data)()

# Determine first column for lookup
first_norm_col = df.columns[0]
first_orig_col = [orig for orig, norm in col_mapping.items() if norm == first_norm_col][0]

# App header
st.title("Lookup by First Column")
st.write(f"Enter a value to match the first column: **{first_orig_col}**")

# Input field
default_placeholder = "e.g. 175"
user_input = st.text_input(first_orig_col, placeholder=default_placeholder)

if user_input:
    # Validate integer input
    try:
        lookup_val = int(user_input)
    except ValueError:
        st.error(f"Please enter a valid integer for {first_orig_col}.")
    else:
        # Filter rows where first column matches
        result = df[df[first_norm_col] == lookup_val]
        if result.empty:
            st.warning(f"No records found where {first_orig_col} = {lookup_val}.")
        else:
            # Show details of the first matched row
            row = result.iloc[0]
            st.subheader(f"Details for {first_orig_col} {lookup_val}")
            for orig_col, norm_col in col_mapping.items():
                st.write(f"**{orig_col}**: {row[norm_col]}")

