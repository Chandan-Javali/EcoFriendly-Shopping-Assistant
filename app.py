import streamlit as st
import pickle
import numpy as np

# Load trained model
with open("ecoshop_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("EcoShop AI - Sustainable Shopping Assistant")
st.write("Enter product details to check if it is eco-friendly.")

# User input fields
material_score = st.slider("Material Score (1-10)", 1, 10, 5)
carbon_footprint_score = st.slider("Carbon Footprint Score (1-10)", 1, 10, 5)
packaging_score = st.slider("Packaging Score (1-10)", 1, 10, 5)
certification_score = st.slider("Certification Score (1-10)", 1, 10, 5)

if st.button("Check Eco-Friendliness"):
    # Prepare input data
    product_features = np.array([[material_score, carbon_footprint_score, packaging_score, certification_score]])
    prediction = model.predict(product_features)
    eco_score = (material_score * 0.3) + (carbon_footprint_score * 0.3) + (packaging_score * 0.2) + (certification_score * 0.2)
    
    # Display results
    if prediction[0] == 1:
        st.success(f"✅ This product is **Eco-Friendly**! (Eco Score: {eco_score:.2f})")
    else:
        st.error(f"❌ This product is **Not Eco-Friendly**. (Eco Score: {eco_score:.2f})")