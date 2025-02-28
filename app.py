import pandas as pd
import streamlit as st
import plotly.express as px
from fuzzywuzzy import process

# Streamlit page setup
st.set_page_config(page_title="EcoShop AI - Sustainable Shopping Assistant", layout="wide")

# Custom HTML & CSS for better UI
def set_page_style():
    st.markdown(
        """
        <style>
        body { background-color: #121212; color: white; }
        .stTextInput>div>div>input { color: white; background-color: #333; }
        .stDataFrame { background-color: #222; color: white; }
        .stButton>button { background-color: #28a745; color: white; }
        </style>
        """,
        unsafe_allow_html=True,
    )

set_page_style()

# Load product data
df = pd.read_csv('products.csv')
df['product_name'] = df['product_name'].str.strip().str.lower()

# Title
st.markdown("""
    <h1 style='text-align: center;'>🌱 EcoShop AI - Sustainable Shopping Assistant</h1>
""", unsafe_allow_html=True)

# User input
product_name = st.text_input("Enter a product name:")

if product_name:
    product_name = product_name.strip().lower()
    result = process.extractOne(product_name, df['product_name'])
    
    if result and result[1] > 80:
        best_match = result[0]
        product_data = df[df['product_name'] == best_match]
        st.subheader(f"Best Match: {best_match.capitalize()}")
        st.dataframe(product_data)
        
        # Sustainability Score Chart
        if 'material_score' in product_data and 'carbon_footprint' in product_data:
            fig = px.bar(
                product_data.melt(id_vars=['product_name'], value_vars=['material_score', 'carbon_footprint']),
                x='variable', y='value', color='variable',
                title=f"Sustainability Scores for {best_match.capitalize()}",
                text_auto=True
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("No close match found. Try a different term.")
