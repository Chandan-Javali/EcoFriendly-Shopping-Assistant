import pandas as pd
import streamlit as st
import plotly.express as px

# Load the product data from the CSV file
df = pd.read_csv('products.csv')  # Make sure the CSV file is in the same directory

# Streamlit page setup
st.set_page_config(page_title="EcoShop AI - Sustainable Shopping Assistant", layout="centered")

# App title and description
st.title("🌱 EcoShop AI - Sustainable Shopping Assistant")
st.markdown("### Check the eco-friendliness of a product based on its sustainability factors.")

# Input field for product name
product_name = st.text_input("Enter product name:")

# Search for the product in the CSV
product_data = df[df['product_name'].str.lower() == product_name.lower()]

if not product_data.empty:
    # Extract the relevant information for the selected product
    material_score = product_data['material_score'].values[0]
    carbon_footprint = product_data['carbon_footprint'].values[0]
    packaging = product_data['packaging'].values[0]
    tips = product_data['tips'].values[0]

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
        title=f"{product_name.capitalize()} Eco-Friendliness Breakdown",
    )
    fig.update_traces(fill='toself', line=dict(color=eco_colors[eco_rating]))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[1, 10])))

    # Show radar chart
    st.plotly_chart(fig)
else:
    st.write("Product not found. Please try a different product.")
