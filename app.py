import streamlit as st
import pandas as pd

# Load the dataset
def load_data():
    file_path = "eco_friendly_products_full.csv"
    df = pd.read_csv(file_path)
    return df

df = load_data()

st.title("🌱 Eco-Friendly Shopping Assistant")

st.markdown("## Please select category")

# Category selection
categories = df['Category'].unique().tolist()
selected_category = st.selectbox("Select category", categories)

# Product input layout
col1, col2 = st.columns([3, 2])
with col1:
    product_name = st.text_input("Product Name", placeholder="Type product name here...")

# Check available products button
selected_product = None
with col2:
    if st.button("🔍 Check Available Products"):
        available_products = df[df['Category'] == selected_category]['Product'].unique().tolist()
        selected_product = st.selectbox("Available Products", available_products, key="available_products")

# If a product is selected from the list, update the product_name field
if selected_product:
    product_name = selected_product

# Display the eco score
def get_eco_score(product):
    row = df[df['Product'].str.lower() == product.lower()]
    if not row.empty:
        return row.iloc[0]['Eco Score']
    return "Not Found"

if product_name:
    eco_score = get_eco_score(product_name)
    st.markdown(f"🌍 **The eco score for {product_name} is: {eco_score}**")
    if eco_score in ["A", "B"]:
        st.success("✅ Excellent eco-friendly choice!")
    else:
        st.error("❌ Not an eco-friendly choice.")


