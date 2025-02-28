<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EcoShop AI - Sustainable Shopping</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body { background-color: #121212; color: white; }
        .container { max-width: 700px; margin-top: 50px; }
        .result-card { background: #1e1e1e; padding: 15px; border-radius: 10px; margin-top: 10px; }
        .eco-score { font-size: 1.5rem; font-weight: bold; color: #4CAF50; }
    </style>
</head>
<body>
    <div class="container text-center">
        <h1>🌱 EcoShop AI</h1>
        <p>Select a category, then search for a product.</p>
        
        <select id="categorySelect" class="form-select">
            <option value="">Select Category</option>
            <option value="electrical">Electrical</option>
            <option value="metal">Metal</option>
            <option value="plastic">Plastic</option>
            <option value="organic">Organic</option>
        </select>
        
        <div class="mt-3">
            <input type="text" id="searchBox" class="form-control" placeholder="Search for a product..." disabled>
            <div id="suggestions" class="list-group mt-2"></div>
        </div>
        
        <div id="productResults" class="mt-4"></div>
    </div>
    
    <script>
        $(document).ready(function() {
            let productData = [];

            $.getJSON("products.json", function(data) {
                productData = data;
            });

            $("#categorySelect").change(function() {
                let category = $(this).val();
                $("#searchBox").prop("disabled", !category);
                $("#searchBox").val("");
                $("#suggestions").empty();
                $("#productResults").empty();
            });

            $("#searchBox").on("input", function() {
                let query = $(this).val().toLowerCase();
                let category = $("#categorySelect").val();
                let matches = productData.filter(p => p.category === category && p.product_name.toLowerCase().includes(query));
                $("#suggestions").empty();
                
                matches.slice(0, 5).forEach(m => {
                    $("#suggestions").append(`<button class='list-group-item list-group-item-action' onclick='showProduct("${m.product_name}")'>${m.product_name}</button>`);
                });
            });
            
            window.showProduct = function(name) {
                let product = productData.find(p => p.product_name === name);
                if (product) {
                    let ecoScore = Math.round((product.material_score * 0.4 + (10 - product.carbon_footprint) * 0.5 + product.packaging * 0.1));
                    let tip = ecoScore >= 8 ? "🌍 Great choice!" : ecoScore >= 5 ? "♻️ Decent option." : "⚠️ Consider a greener choice.";
                    
                    $("#productResults").html(`
                        <div class='result-card'>
                            <h3>${product.product_name}</h3>
                            <p class='eco-score'>Eco Score: ${ecoScore}/10</p>
                            <p><strong>Material Score:</strong> ${product.material_score}</p>
                            <p><strong>Carbon Footprint:</strong> ${product.carbon_footprint}</p>
                            <p><strong>Packaging:</strong> ${product.packaging}</p>
                            <p><strong>Tip:</strong> ${tip}</p>
                        </div>
                    `);
                }
                $("#suggestions").empty();
            };
        });
    </script>
</body>
</html>


