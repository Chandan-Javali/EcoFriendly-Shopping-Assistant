import streamlit as st
import pandas as pd
from fuzzywuzzy import process

# Page Config
st.set_page_config(page_title="EcoShop AI", layout="wide")

# Load Product Data
@st.cache_data
def load_data():
    df = pd.read_csv("products.csv")
    df["product_name"] = df["product_name"].str.strip().str.lower()
    return df

df = load_data()

# Custom CSS for styling
st.markdown("""
    <style>
        body { background-color: #121212; color: white; font-family: Arial, sans-serif; }
        .search-container { margin: 50px auto; max-width: 600px; }
        .search-box { width: 100%; padding: 10px; border-radius: 5px; background: #1e1e1e; color: white; border: 1px solid #444; }
        .search-box::placeholder { color: #bbb; }
        .result-card { background: #1e1e1e; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: left; }
    </style>
""", unsafe_allow_html=True)

# UI - Title
st.markdown("<h1 style='text-align: center;'>🌱 EcoShop AI - Sustainable Shopping Assistant</h1>", unsafe_allow_html=True)

# Search Box
product_name = st.text_input("Enter a product name:", "").strip().lower()

if product_name:
    best_match = process.extractOne(product_name, df["product_name"])

    if best_match and best_match[1] > 75:
        matched_product = df[df["product_name"] == best_match[0]].iloc[0]
        
        # Display product details
        st.markdown(f"""
            <div class='result-card'>
                <h2>{matched_product["product_name"].capitalize()}</h2>
                <p><strong>Material Score:</strong> {matched_product["material_score"]}</p>
                <p><strong>Carbon Footprint:</strong> {matched_product["carbon_footprint"]}</p>
                <p><strong>Packaging:</strong> {matched_product["packaging"]}</p>
                <p><strong>Tip:</strong> {matched_product["tips"]}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No close match found. Try another search term.")

