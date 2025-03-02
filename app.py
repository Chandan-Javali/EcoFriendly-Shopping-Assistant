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

# Product name input field (with session state to store selected product)
if "selected_product" not in st.session_state:
    st.session_state.selected_product = ""

col1, col2, col3 = st.columns([3, 1.5, 2.5])

with col1:
    product_name = st.text_input("Product Name", value=st.session_state.selected_product, key="product_input", placeholder="Type product name here...")

with col2:
    st.write("")  # Spacer to align with input field
    if st.button("🔍 Check Available Products"):
        st.session_state.show_dropdown = True  # Set flag to show dropdown

with col3:
    if st.session_state.get("show_dropdown", False):  # Show dropdown only after clicking the button
        available_products = df[df["Category"] == category]["Product Name"].unique()
        selected_product = st.selectbox("Available Products", available_products, key="product_dropdown")

        if selected_product:
            st.session_state.selected_product = selected_product  # Save selected product in session state
            st.experimental_rerun()  # Refresh the UI to update the input field

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


