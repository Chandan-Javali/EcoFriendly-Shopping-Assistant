import streamlit as st
import pandas as pd

def load_data():
    return pd.read_csv("structured_products.csv")

def calculate_eco_score(row):
    return round((row['material_score'] * 0.4 + (10 - row['carbon_footprint']) * 0.5 + row['packaging'] * 0.1))

df = load_data()

st.title("🌱 Eco-Friendly Shopping")
st.write("Select a category, then search for a product.")

# Adjusting category selection to appear below
selected_category = st.selectbox("Choose a Category:", df['category'].unique(), index=0, key="category_selector")

search_query = st.text_input("Search for a product:")
filtered_df = df[(df['category'] == selected_category) & (df['product_name'].str.contains(search_query, case=False, na=False))]

if not filtered_df.empty:
    for _, row in filtered_df.iterrows():
        eco_score = calculate_eco_score(row)
        st.subheader(row['product_name'])
        st.write(f"**Category:** {row['category']}")
        st.write(f"**Eco Score:** {eco_score}/10")
        st.write(f"**Sustainability Tip:** {row['tip']}")
else:
    st.write("No products found. Try another search!")


