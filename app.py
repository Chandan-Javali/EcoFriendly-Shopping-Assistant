import streamlit as st
import pandas as pd

# Load dataset
def load_data():
    return pd.read_csv("eco_friendly_products_full.csv")

def get_eco_details(category, product_name, df):
    product_name = product_name.strip().lower()  # Normalize user input
    df["Product Name"] = df["Product Name"].str.strip().str.lower()  # Normalize dataset
    
    filtered_df = df[(df["Category"] == category) & (df["Product Name"] == product_name)]
    
    if not filtered_df.empty:
        return filtered_df.iloc[0]["Eco Score"], filtered_df.iloc[0]["Tip"]
    return "Not Found", "No sustainability tips available."

# Streamlit UI
st.set_page_config(page_title="Eco-Friendly Shopping Assistant", layout="centered")
st.title("🌱 Eco-Friendly Shopping Assistant")

# Load data
df = load_data()

# Category selection
st.markdown("### Please select category")
category = st.selectbox("Select category", df["Category"].unique())

# Interactive product selection
col1, col2 = st.columns([3, 2])  # Create two columns for better UI

with col1:
    product_name = st.text_input("Product Name", placeholder="Type product name here...")

with col2:
    if st.button("🔍 Check Available Products"):
        available_products = df[df["Category"] == category]["Product Name"].unique()
        selected_product = st.selectbox("Available Products", available_products, key="product_dropdown")
        if selected_product:
            st.session_state.product_name = selected_product  # Auto-fill the text input

# Auto-fill the text input when a product is selected
if "product_name" in st.session_state:
    product_name = st.session_state.product_name
    st.session_state.pop("product_name")  # Clear session state after use

# Display eco-score and eco tips
if product_name:
    eco_score, eco_tip = get_eco_details(category, product_name, df)
    st.markdown(f"### 🌍 The eco score for **{product_name}** is: **{eco_score}**")
    
    if eco_score == "A":
        st.success("✅ Excellent eco-friendly choice!")
    elif eco_score == "B":
        st.info("⚡ Good choice, but can be better.")
    elif eco_score == "C":
        st.warning("⚠️ Consider a more sustainable alternative.")
    else:
        st.error("❌ Not an eco-friendly choice.")
    
    # Display sustainability tip
    st.markdown(f"**♻️ Eco Tip:** {eco_tip}")

