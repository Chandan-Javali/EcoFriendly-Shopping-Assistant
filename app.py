import pandas as pd
import streamlit as st

# Load the product data
@st.cache_data
def load_data():
    df = pd.read_csv("products_updated_v2.csv")
    df.drop_duplicates(subset=['Product Name'], keep='first', inplace=True)  # Ensure unique items
    return df

data = load_data()

# Function to calculate eco score
def calculate_eco_score(row):
    try:
        return round((row['Material Score'] * 0.4 + (10 - row['Carbon Footprint']) * 0.5 + row['Packaging'] * 0.1))
    except KeyError:
        return None

st.title("Eco-Friendly Shopping")

st.write("Select a category, then search for a product.")

# Dropdown to select category
categories = data['Category'].unique()
selected_category = st.selectbox("Choose a Category:", categories, index=0)

# Search bar for product search
search_query = st.text_input("Search for a product:")

# Filter data based on selection
filtered_data = data[data['Category'] == selected_category]

if search_query:
    search_results = filtered_data[filtered_data['Product Name'].str.contains(search_query, case=False, na=False)]
    if not search_results.empty:
        best_match = search_results.iloc[0]  # Show only one best match
        st.subheader(best_match['Product Name'])
        st.write(f"**Category:** {best_match['Category']}")
        eco_score = calculate_eco_score(best_match)
        st.write(f"**Eco Score:** {eco_score}/10")
        st.write(f"**Sustainability Tip:** {best_match['Sustainability Tip']}")
    else:
        st.write("No matching products found.")

