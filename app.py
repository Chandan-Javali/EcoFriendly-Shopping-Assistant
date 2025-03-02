import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the dataset
def load_data():
    file_path = "eco_friendly_products_full.csv"
    df = pd.read_csv(file_path)
    return df

df = load_data()

st.title("\U0001F331 Eco-Friendly Shopping Assistant")

st.markdown("## Please select category")

# Category selection
categories = df['Category'].unique().tolist()
selected_category = st.selectbox("Select category", categories)

# Initialize session state for product_name
if "product_name" not in st.session_state:
    st.session_state.product_name = ""

# Product selection layout
col1, col2 = st.columns([3, 2])

with col1:
    product_name = st.text_input("Product Name", value=st.session_state.product_name, key="product_name_input")

with col2:
    available_products = df[df['Category'] == selected_category]['Product'].unique().tolist()
    selected_product = st.selectbox("Available Products", [""] + available_products, key="available_products")

# Sync text input with selected product
if selected_product:
    st.session_state.product_name = selected_product
elif product_name:
    st.session_state.product_name = product_name

# Function to get eco score and tip
def get_product_info(product):
    row = df[df['Product'].str.lower() == product.lower()]
    if not row.empty:
        return row.iloc[0]['Eco-Score'], row.iloc[0].get('Sustainability Tip', "No tip available")
    return "Not Found", "No tip available"

# Display the eco score and tip
if st.session_state.product_name:
    eco_score, tip = get_product_info(st.session_state.product_name)
    st.markdown(f"\U0001F30D **The eco score for {st.session_state.product_name} is: {eco_score}**")
    if eco_score in ["1", "2"]:
        st.success("✅ Excellent eco-friendly choice!")
    elif eco_score in ["3"]:
        st.warning("⚠️ Moderate eco-friendly choice.")
    else:
        st.error("❌ Not an eco-friendly choice.")
    st.info(f"💡 Tip: {tip}")

    # Plotting
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = int(eco_score) if eco_score.isdigit() else 0, # convert score to int if possible
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Selected Product Eco-Score"},
        gauge = {'axis': {'range': [None, 5]},
                 'bar': {'color': "darkblue"},
                 'steps' : [
                     {'range': [0, 2], 'color': "lightgreen"},
                     {'range': [2, 3], 'color': "yellow"},
                     {'range': [3, 5], 'color': "red"}]}))
    st.plotly_chart(fig)

    fig_ideal = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 1, # Ideal eco score is 1
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Ideal Eco-Score"},
        gauge = {'axis': {'range': [None, 5]},
                 'bar': {'color': "darkblue"},
                 'steps' : [
                     {'range': [0, 2], 'color': "lightgreen"},
                     {'range': [2, 3], 'color': "yellow"},
                     {'range': [3, 5], 'color': "red"}]}))
    st.plotly_chart(fig_ideal)
