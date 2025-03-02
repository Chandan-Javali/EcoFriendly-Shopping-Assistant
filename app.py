import streamlit as st
import pandas as pd

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("eco_friendly_products.csv")

df = load_data()

# Streamlit UI
st.title("🌱 Eco-Friendly Shopping Assistant")

# Select category
category = st.selectbox("Choose a Category:", df["Category"].unique())

# Enter product name
product_name = st.text_input("Search for a product:").strip()

# Display product details
if product_name:
    filtered_df = df[(df["Category"] == category) & (df["Product Name"].str.contains(product_name, case=False, na=False))]
    
    if not filtered_df.empty:
        for _, row in filtered_df.iterrows():
            st.markdown(f"**Product:** {row['Product Name']}")
            st.markdown(f"**Eco Score:** {row['Eco Score']}/10")
            
            # Sustainability Tip
            if row['Eco Score'] >= 8:
                tip = "Great choice! This product is highly eco-friendly. Consider repairing instead of replacing."
            elif row['Eco Score'] >= 5:
                tip = "This product has a moderate eco-score. Look for energy-efficient or recycled options."
            else:
                tip = "Low eco-score! Try to find alternatives with better sustainability ratings."
            
            st.info(tip)
    else:
        st.warning("No matching products found. Try a different search.")
