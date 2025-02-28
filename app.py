import streamlit as st
import plotly.express as px

# Streamlit page setup
st.set_page_config(page_title="EcoShop AI - Sustainable Shopping Assistant", layout="centered")

# App title and description
st.title("🌱 EcoShop AI - Sustainable Shopping Assistant")
st.markdown("### Check the eco-friendliness of a product based on its sustainability factors.")

# Product Name Input
product_name = st.text_input("Enter Product Name", "")

# If product name is provided, show the analysis section
if product_name:
    # Sliders for scores (Material, Carbon Footprint, Packaging)
    material = st.slider("Material Score (1-10)", 1, 10, 5)
    carbon = st.slider("Carbon Footprint Score (1-10)", 1, 10, 5)
    packaging = st.slider("Packaging Score (1-10)", 1, 10, 5)
    
    # Calculate total eco-score
    total_score = round((material + carbon + packaging) / 3, 1)
    eco_rating = "Eco-Friendly" if total_score > 7 else "Moderate" if total_score > 4 else "Not Eco-Friendly"
    
    # Display the results
    st.subheader(f"Eco Score for {product_name}:")
    st.metric(label="Overall Score", value=f"{total_score}/10")
    st.markdown(f"**Eco-Friendliness Rating: {eco_rating}**")
    
    # Additional tips based on rating
    if eco_rating == "Eco-Friendly":
        st.markdown("✅ **This product is eco-friendly!** Consider looking for certifications such as Fair Trade or Organic.")
    elif eco_rating == "Moderate":
        st.markdown("⚖️ **This product has a moderate eco-impact.** Consider ways to reduce its carbon footprint like recycling or reusing.")
    else:
        st.markdown("❌ **This product is not eco-friendly.** Try to switch to alternatives with a lower carbon footprint, minimal packaging, or sustainable materials.")
    
    # Color mapping for chart
    eco_colors = {"Eco-Friendly": "green", "Moderate": "orange", "Not Eco-Friendly": "red"}
    
    # Radar chart data
    fig = px.line_polar(
        r=[material, carbon, packaging, material],
        theta=["Material", "Carbon Footprint", "Packaging", "Material"],
        line_close=True,
        markers=True,
        title=f"{product_name} Eco-Friendliness Breakdown",
    )
    fig.update_traces(fill='toself', line=dict(color=eco_colors[eco_rating]))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[1, 10])))
    
    # Show radar chart
    st.plotly_chart(fig)

    # Visualization of each component
    st.subheader("Detailed Component Scores")
    components = ['Material', 'Carbon Footprint', 'Packaging']
    scores = [material, carbon, packaging]
    st.bar_chart({component: score for component, score in zip(components, scores)})

else:
    st.warning("Please enter a product name to start analyzing its eco-friendliness!")
