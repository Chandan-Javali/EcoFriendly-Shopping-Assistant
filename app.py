import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="EcoShop AI", layout="wide")

# Load CSV and convert to JSON
@st.cache_data
def load_data():
    df = pd.read_csv("products.csv")
    return df.to_dict(orient="records")

data = load_data()
json_data = json.dumps(data)

# Inject HTML, CSS, and JavaScript
st.markdown(f"""
    <script>
        var productData = {json_data};

        function searchProduct() {{
            let query = document.getElementById("searchBox").value.toLowerCase();
            let suggestions = document.getElementById("suggestions");
            suggestions.innerHTML = '';

            let matches = productData.filter(p => p.product_name.includes(query));
            matches.slice(0, 5).forEach(m => {{
                let btn = document.createElement('button');
                btn.className = 'list-group-item list-group-item-action suggestion-item';
                btn.innerText = m.product_name;
                btn.onclick = function() {{ showProduct(m); }};
                suggestions.appendChild(btn);
            }});
        }}

        function showProduct(product) {{
            document.getElementById("productResults").innerHTML = `
                <div class='result-card'>
                    <h2>${{product.product_name}}</h2>
                    <p><strong>Material Score:</strong> ${{product.material_score}}</p>
                    <p><strong>Carbon Footprint:</strong> ${{product.carbon_footprint}}</p>
                    <p><strong>Packaging:</strong> ${{product.packaging}}</p>
                    <p><strong>Tip:</strong> ${{product.tips}}</p>
                </div>
            `;
            document.getElementById("suggestions").innerHTML = '';
        }}
    </script>

    <div class="container text-center">
        <h1 class="mt-4">🌱 EcoShop AI - Sustainable Shopping Assistant</h1>
        <div class="search-container">
            <input type="text" id="searchBox" class="form-control search-box" placeholder="🔍 Search for a product..." oninput="searchProduct()">
            <div id="suggestions" class="list-group mt-2"></div>
        </div>
        <div id="productResults" class="mt-4"></div>
    </div>

    <style>
        body {{ background-color: #121212; color: white; font-family: Arial, sans-serif; }}
        .search-container {{ margin: 50px auto; max-width: 600px; }}
        .search-box {{ background: #1e1e1e; color: white; padding: 10px; border-radius: 5px; border: 1px solid #444; }}
        .search-box::placeholder {{ color: #bbb; }}
        .list-group-item {{ background: #1e1e1e; color: white; border: none; cursor: pointer; transition: 0.3s; }}
        .list-group-item:hover {{ background: #333; }}
        .result-card {{ background: #1e1e1e; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: left; }}
    </style>
""", unsafe_allow_html=True)
