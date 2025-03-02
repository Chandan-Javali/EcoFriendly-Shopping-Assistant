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

# Search functionality
search_query = st.text_input("🔍 Search for a product")
if search_query:
    search_results = df[df['Product Name'].str.contains(search_query, case=False, na=False)]['Product Name'].tolist()
    if search_results:
        st.write("### Search Results")
        st.write(search_results)
    else:
        st.write("No matching products found.")

# Function to get eco score and tip
def get_eco_details(product):
    row = df[df['Product Name'].str.lower() == product.lower()]
    if not row.empty:
        return row.iloc[0]['Eco Score'], row.iloc[0].get('Eco Tip', "No tip available.")
    return "Not Found", "No tip available."

# Display the eco score and tip
if st.session_state.product_name:
    eco_score, eco_tip = get_eco_details(st.session_state.product_name)
    st.markdown(f"🌍 **The eco score for {st.session_state.product_name} is: {eco_score}**")
    st.markdown(f"💡 **Tip:** {eco_tip}")
    if eco_score in ["A", "B"]:
        st.success("✅ Excellent eco-friendly choice!")
    else:
        st.error("❌ Not an eco-friendly choice.")

