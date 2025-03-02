import streamlit as st
import pandas as pd

def load_data():
    df = pd.read_csv("structured_products.csv")
    df.drop_duplicates(subset=['product_name'], keep='first', inplace=True)  # Ensure unique items
    return df

data = load_data()

st.title("Eco-Friendly Shopping Assistant")

# Move category selection to bottom
search_query = st.text_input("Search for a product:")
selected_category = st.selectbox("Choose a Category:", sorted(data["category"].unique()))

filtered_data = data[(data["category"] == selected_category) & (data["product_name"].str.contains(search_query, case=False, na=False))]

if not filtered_data.empty:
    product = filtered_data.iloc[0]  # Ensure only one product is shown
    st.markdown(f"""
    ## {product['product_name']}
    **Category:** {product['category']}  
    **Eco Score:** {product['eco_score']}/10  
    **Sustainability Tip:** {product['sustainability_tip']}  
    """)
else:
    st.write("No products found.")

st.markdown("---")
st.subheader("Categories")
st.write(sorted(data["category"].unique()))

