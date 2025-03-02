import streamlit as st
import pandas as pd

# Load dataset
def load_data():
    return pd.read_csv("eco_friendly_products_full.csv")  # Make sure this file includes "Eco Tips" column

def get_eco_details(category, product_name, df):
    filtered_df = df[(df["Category"] == category) & (df["Product Name"].str.lower() == product_name.lower())]
    if not filtered_df.empty:
        return filtered_df.iloc[0]["Eco Score"], filtered_df.iloc[0]["Eco Tips"]
    return "Not Found", "No sustainability tips available."

# Streamlit UI
st.set_page_config(page_title="Eco-Friendly Shopping Assistant", layout="centered")
st.title("🌱 Eco-Friendly Shopping Assistant")

# Load data
df = load_data()

# Category selection
st.markdown("### Please select category")
category = st.selectbox("Select category", df["Category"].unique())

# Product input
st.markdown("### Enter the product name below")
product_name = st.text_input("Product Name", placeholder="Type product name here...")

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

