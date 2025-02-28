import pandas as pd
import streamlit as st
import plotly.express as px
from fuzzywuzzy import process

# Load the product data from the CSV file
df = pd.read_csv('products.csv')

# Ensure product names are stripped of whitespace and case-insensitive
df['product_name'] = df['product_name'].str.strip().str.lower()

# Streamlit page setup
st.set_page_config(page_title="EcoShop AI - Sustainable Shopping Assistant", layout="centered")

# App title and description
st.title("\U0001F331 EcoShop AI - Sustainable Shopping Assistant")
st.markdown("### Check the eco-friendliness of a product based on its sustainability factors.")

# Input field for product name
product_name = st.text_input("Enter product name:").strip().lower()

if product_name:
    # Find the best match for the input
    best_match, score = process.extractOne(product_name, df['product_name'])
    if score > 80:
        product_data = df[df['product_name'] == best_match]
    else:
        product_data = pd.DataFrame()
else:
    product_data = pd.DataFrame()

if not product_data.empty:
    # Extract the relevant information for the selected product
    material_score = product_data.iloc[0]['material_score']
    carbon_footprint = product_data.iloc[0]['carbon_footprint']
    packaging = product_data.iloc[0]['packaging']
    tips = product_data.iloc[0]['tips']

    # Calculate total eco-score
    total_score = round((material_score + carbon_footprint + packaging) / 3, 1)
    eco_rating = "Eco-Friendly" if total_score > 7 else "Moderate" if total_score > 4 else "Not Eco-Friendly"

    # Display results
    st.subheader("Eco Score: ")
    st.metric(label="Overall Score", value=f"{total_score}/10", delta=None)
    st.markdown(f"**Eco-Friendliness Rating: {eco_rating}**")
    st.markdown(f"**Tips for this product:** {tips}")

    # Radar chart data
    eco_colors = {"Eco-Friendly": "green", "Moderate": "orange", "Not Eco-Friendly": "red"}

    fig = px.line_polar(
        r=[material_score, carbon_footprint, packaging, material_score],
        theta=["Material", "Carbon Footprint", "Packaging", "Material"],
        line_close=True,
        markers=True,
        title=f"{best_match.capitalize()} Eco-Friendliness Breakdown",
    )
    fig.update_traces(fill='toself', line=dict(color=eco_colors[eco_rating]))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[1, 10])))

    # Show radar chart
    st.plotly_chart(fig)
else:
    st.write("Product not found. Please check the name or try a different product.")
