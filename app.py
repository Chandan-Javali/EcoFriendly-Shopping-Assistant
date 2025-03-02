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

# Product selection
col1, col2 = st.columns([3, 2])
with col1:
    product_name = st.text_input("Product Name", placeholder="Type product name here...")

with col2:
    if st.button("🔍 Check Available Products", key="check_products"):
        available_products = df[df['Category'] == selected_category]['Product Name'].unique().tolist()
        selected_product = st.selectbox("Available Products", available_products, key="available_products")

        # Auto-fill product name field
        product_name = selected_product

# Display the eco score
def get_eco_score(product):
    row = df[df['Product Name'].str.lower() == product.lower()]
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


