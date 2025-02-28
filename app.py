import pandas as pd
import streamlit as st
import plotly.express as px
from fuzzywuzzy import process  # Ensure this is installed

# Streamlit page setup (This must be the first Streamlit command)
st.set_page_config(page_title="EcoShop AI - Sustainable Shopping Assistant")

# Load the product data from the CSV file
df = pd.read_csv('products.csv')
df['product_name'] = df['product_name'].str.strip().str.lower()

# App title and description
st.title("🌱 EcoShop AI - Sustainable Shopping Assistant")

# User input for product search
product_name = st.text_input("Enter a product name:")

if product_name:
    # Ensure case and whitespace consistency
    product_name = product_name.strip().lower()

    # Find the best match for the input
    result = process.extractOne(product_name, df['product_name'])

    if result:
        best_match, score = result[0], result[1]
        if score > 80:
            product_data = df[df['product_name'] == best_match]
            st.write("Best match:", best_match)
            st.dataframe(product_data)
        else:
            st.write("No close match found.")
    else:
        st.write("No matches found.")

