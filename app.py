import streamlit as st
import pandas as pd

def load_data():
    return pd.read_csv("products_updated_v2.csv")

def calculate_eco_score(row):
    return round((row['Material Score'] * 0.4 + (10 - row['Carbon Footprint']) * 0.5 + row['Packaging'] * 0.1))

st.set_page_config(page_title="EcoShop AI", layout="centered")
st.title("🌱 EcoShop AI - Sustainable Shopping")
st.write("Select a category, then search for a product.")

data = load_data()
categories = sorted(data['Category'].unique().tolist())
categories.insert(0, "Select Category")

selected_category = st.selectbox("Choose a Category:", categories)

if selected_category != "Select Category":
    search_query = st.text_input("Search for a product:")
    if search_query:
        filtered_products = data[(data['Category'] == selected_category) & 
                                 (data['Product Name'].str.contains(search_query, case=False, na=False))]
        
        if not filtered_products.empty:
            for _, row in filtered_products.iterrows():
                eco_score = calculate_eco_score(row)
                tip = "🌍 Great choice!" if eco_score >= 8 else "♻️ Decent option." if eco_score >= 5 else "⚠️ Consider a greener choice."
                
                st.markdown(f"""
                <div style='background:#1e1e1e;padding:15px;border-radius:10px;margin-top:10px;'>
                    <h3>{row['Product Name']}</h3>
                    <p style='color:#4CAF50;font-size:1.5rem;font-weight:bold;'>Eco Score: {eco_score}/10</p>
                    <p><strong>Material Score:</strong> {row['Material Score']}</p>
                    <p><strong>Carbon Footprint:</strong> {row['Carbon Footprint']}</p>
                    <p><strong>Packaging:</strong> {row['Packaging']}</p>
                    <p><strong>Tip:</strong> {tip}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No products found. Try another search!")


