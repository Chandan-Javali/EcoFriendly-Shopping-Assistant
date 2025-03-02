import streamlit as st
import pandas as pd

# Load dataset
def load_data():
    return pd.read_csv("eco_friendly_products_expanded.csv")

def get_eco_score(category, product_name, df):
    filtered_df = df[(df["Category"] == category) & (df["Product Name"].str.lower() == product_name.lower())]
    if not filtered_df.empty:
        return filtered_df.iloc[0]["Eco Score"]
    return "Not Found"

# Streamlit UI
st.set_page_config(page_title="Eco-Friendly Shopping Assistant", layout="centered")
st.title("🌱 Eco-Friendly Shopping Assistant")

# Load data
df = load_data()

# Category selection with animation effect
st.markdown("### Please select category")
category = st.selectbox("Select category", df["Category"].unique())

# Product input with dropdown effect
st.markdown("### Enter the product name below")
product_name = st.text_input("Product Name", placeholder="Type product name here...")

# Display eco-score with better UI
if product_name:
    eco_score = get_eco_score(category, product_name, df)
    st.markdown(f"### 🌍 The eco score for **{product_name}** is: **{eco_score}**")
    if eco_score == "A":
        st.success("✅ Excellent eco-friendly choice!")
    elif eco_score == "B":
        st.info("⚡ Good choice, but can be better.")
    elif eco_score == "C":
        st.warning("⚠️ Consider a more sustainable alternative.")
    else:
        st.error("❌ Not an eco-friendly choice.")

