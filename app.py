import streamlit as st
import pandas as pd

# Load the dataset
def load_data():
    file_path = "eco_friendly_products_full.csv"
    df = pd.read_csv(file_path)
    return df

df = load_data()

st.title("\U0001F331 Eco-Friendly Shopping Assistant")

st.markdown("## Please select category")

# Category selection
categories = df['Category'].unique().tolist()
selected_category = st.selectbox("Select category", categories)

# Initialize session state for product_name
if "product_name" not in st.session_state:
    st.session_state.product_name = ""

# Product selection layout
col1, col2 = st.columns([3, 2])

with col2:
    available_products = df[df['Category'] == selected_category]['Product Name'].unique().tolist()
    selected_product = st.selectbox("Available Products", [""] + available_products, key="available_products")

# Sync text input with selected product
if selected_product:
    st.session_state.product_name = selected_product

with col1:
    product_name = st.text_input("Product Name", value=st.session_state.product_name, key="product_name_input")

# Function to get eco score and tip
def get_product_info(product):
    row = df[df['Product Name'].str.lower() == product.lower()]
    if not row.empty:
        return row.iloc[0]['Eco Score'], row.iloc[0].get('Tip', "No tip available")
    return "Not Found", "No tip available"

# Display the eco score and tip
if st.session_state.product_name:
    eco_score, tip = get_product_info(st.session_state.product_name)
    st.markdown(f"\U0001F30D **The eco score for {st.session_state.product_name} is: {eco_score}**")
    if eco_score in ["A", "B"]:
        st.success("✅ Excellent eco-friendly choice!")
    else:
        st.error("❌ Not an eco-friendly choice.")
    st.info(f"💡 Tip: {tip}")


