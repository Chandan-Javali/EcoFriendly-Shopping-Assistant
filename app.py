import streamlit as st
import pandas as pd

def load_data():
    try:
        df = pd.read_csv("eco_friendly_products.csv")
        df.fillna("No Data", inplace=True)  # Avoid empty values breaking the UI
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def main():
    st.set_page_config(page_title="Eco-Friendly Shopping Assistant", layout="wide")
    st.title("🌱 Eco-Friendly Shopping Assistant")

    df = load_data()
    if df.empty:
        st.warning("No data available. Check your CSV file.")
        return

    category = st.selectbox("Choose a Category:", options=df["Category"].unique())
    search_query = st.text_input("Search for a product:").strip().lower()

    filtered_df = df[df["Category"] == category]
    if search_query:
        filtered_df = filtered_df[filtered_df["Product"].str.lower().str.contains(search_query, na=False)]

    if not filtered_df.empty:
        st.write("### Matching Products")
        st.dataframe(filtered_df[['Product', 'Price', 'Eco Score', 'Tip']])
    else:
        st.warning("No matching products found. Try another search term.")

if __name__ == "__main__":
    main()

