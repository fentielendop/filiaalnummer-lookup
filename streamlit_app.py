import streamlit as st
import pandas as pd

# Configure page for mobile-friendly layout
st.set_page_config(
    page_title="Filiaalnummer Lookup",
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
    # Create mapping of original to normalized
    col_mapping = dict(zip(original_cols, normalized_cols))
    return df, col_mapping

# Cache the data and get mapping
df, col_mapping = st.cache_data(load_data)()

# Debug: show original vs normalized columns
with st.expander("View Data Columns"):
    st.write(col_mapping)

# App title
st.title("Filiaalnummer Lookup App")
st.write("Enter a filiaalnummer to see all information on that row.")

# Input field for the filiaalnummer
fil_num = st.text_input("Filiaalnummer", placeholder="e.g. 12345")

# Normalized column name to search
column_name = 'filiaalnummer'

if fil_num:
    # Validate input
    try:
        fil_num_val = int(fil_num)
    except ValueError:
        st.error("Please enter a valid integer for filiaalnummer.")
    else:
        # Check column exists
        if column_name not in df.columns:
            st.error(f"Column '{column_name}' not found. Check the column list above.")
        else:
            # Filter rows
            result = df[df[column_name] == fil_num_val]
            if result.empty:
                st.warning(f"No records found for filiaalnummer {fil_num_val}.")
            else:
                # If single match, show details vertically
                if len(result) == 1:
                    row = result.iloc[0]
                    st.subheader(f"Details for filiaalnummer {fil_num_val}")
                    for orig_col, norm_col in col_mapping.items():
                        value = row[norm_col]
                        st.write(f"**{orig_col}**: {value}")
                else:
                    # Multiple matches: show full table
                    st.subheader(f"Multiple records for filiaalnummer {fil_num_val}")
                    st.dataframe(result)

# Instructions for running the app
st.markdown("---")
st.markdown(
    "**How to run:**\n"
    "1. Convert `klantenlijst.xls` to `klantenlijst.xlsx` in Excel.\n"
    "2. Ensure `klantenlijst.xlsx` is in the same directory as this script.\n"
    "3. Install dependencies: `pip install streamlit pandas openpyxl`\n"
    "4. Run the app with: `streamlit run streamlit_app.py`"
)
