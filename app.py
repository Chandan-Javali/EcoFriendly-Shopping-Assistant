import streamlit as st
import pandas as pd

# Load data
def load_data():
    try:
        df = pd.read_csv("eco_friendly_products.csv")
        df.columns = df.columns.str.strip()  # Remove any unwanted spaces in column names
        return df
    except FileNotFoundError:
        st.error("Error: eco_friendly_products.csv file not found.")
        return None

df = load_data()

# UI Improvements - Dark theme and better layout
st.set_page_config(page_title="Eco-Friendly Shopping Assistant", layout="wide")
st.markdown(
    """
    <style>
        body {
            background-color: #121212;
            color: white;
            font-family: Arial, sans-serif;
        }
        .stTextInput>div>div>input {
            background-color: #333;
            color: white;
            border-radius: 8px;
        }
        .stSelectbox>div>div>select {
            background-color: #333;
            color: white;
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌿 Eco-Friendly Shopping Assistant")

if df is not None:
    # Dropdown for category selection
    categories = df['Category'].unique().tolist()
    category = st.selectbox("Choose a Category:", ["All"] + categories)
    
    # Search box for product name
    search_query = st.text_input("Search for a product:").strip().lower()
    
    # Filter data based on selection
    if category != "All":
        df_filtered = df[df['Category'] == category]
    else:
        df_filtered = df
    
    if search_query:
        df_filtered = df_filtered[df_filtered['Product Name'].str.lower().str.contains(search_query, na=False)]
    
    # Display results
    if not df_filtered.empty:
        st.dataframe(df_filtered[['Product Name', 'Brand', 'Price', 'Sustainability Score']])
    else:
        st.warning("No matching products found. Try another search term.")

