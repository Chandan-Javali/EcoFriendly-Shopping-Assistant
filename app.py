import streamlit as st
import plotly.express as px

# Streamlit page setup
st.set_page_config(page_title="EcoShop AI - Sustainable Shopping Assistant", layout="centered")

# App title and description
st.title("🌱 EcoShop AI - Sustainable Shopping Assistant")
st.markdown("### Check the eco-friendliness of a product based on its sustainability factors.")

# Sliders for scores
material = st.slider("Material Score (1-10)", 1, 10, 5)
carbon = st.slider("Carbon Footprint Score (1-10)", 1, 10, 5)
packaging = st.slider("Packaging Score (1-10)", 1, 10, 5)

# Calculate total eco-score
total_score = round((material + carbon + packaging) / 3, 1)
eco_rating = "Eco-Friendly" if total_score > 7 else "Moderate" if total_score > 4 else "Not Eco-Friendly"

# Display results
st.subheader("Eco Score: ")
st.metric(label="Overall Score", value=f"{total_score}/10", delta=None)
st.markdown(f"**Eco-Friendliness Rating: {eco_rating}**")

# Color mapping for chart
eco_colors = {"Eco-Friendly": "green", "Moderate": "orange", "Not Eco-Friendly": "red"}

# Radar chart data
fig = px.line_polar(
    r=[material, carbon, packaging, material],
    theta=["Material", "Carbon Footprint", "Packaging", "Material"],
    line_close=True,
    markers=True,
    title="Eco-Friendliness Breakdown",
)
fig.update_traces(fill='toself', line=dict(color=eco_colors[eco_rating]))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[1, 10])))

# Show radar chart
st.plotly_chart(fig)
