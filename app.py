import streamlit as st
import pandas as pd

# Set the page configuration
st.set_page_config(page_title="CSV Importer", page_icon="📊", layout="wide")

# Load custom CSS for styling
def load_css():
    with open("styles/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Title of the app
st.title("CSV File Importer")
st.markdown("Upload your CSV file to view its contents.")

# File uploader for CSV files
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    
    # Display the dataframe
    st.write("### Data Preview:")
    st.dataframe(df)

    # Display basic statistics
    st.write("### Basic Statistics:")
    st.write(df.describe())

    # Optionally, display the shape of the dataframe
    st.write("### Data Shape:")
    st.write(df.shape)