import streamlit as st
import pandas as pd

# Load data
def load_data():
    try:
        return pd.read_csv("eco_friendly_products.csv")
    except FileNotFoundError:
        st.error("Error: The dataset file 'eco_friendly_products.csv' was not found. Please upload it or check the file path.")
        return pd.DataFrame()

df = load_data()

st.title("Eco-Friendly Shopping Assistant")

# Select category
category = st.selectbox("Choose a Category:", df["Category"].unique() if not df.empty else [])

# Search bar for product name
search_query = st.text_input("Search for a product:")

if search_query:
    results = df[(df["Category"] == category) & (df["Product Name"].str.contains(search_query, case=False, na=False))]
    
    if not results.empty:
        for _, product in results.iterrows():
            st.subheader(product["Product Name"])
            st.write(f"**Eco Score:** {product['Eco Score']}/10")
            st.write(f"**Sustainability Tip:** {product['Sustainability Tip']}")
    else:
        st.warning("No matching products found. Try another search term.")
