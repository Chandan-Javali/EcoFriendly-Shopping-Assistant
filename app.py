<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EcoShop AI - Sustainable Shopping Assistant</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body { background-color: #121212; color: white; }
        .search-container { margin: 50px auto; max-width: 600px; }
        .result-card { background: #1e1e1e; padding: 15px; border-radius: 10px; margin-top: 10px; }
        .eco-score { font-size: 1.5rem; font-weight: bold; color: #4CAF50; }
    </style>
</head>
<body>
    <div class="container text-center">
        <h1 class="mt-4">🌱 EcoShop AI - Sustainable Shopping Assistant</h1>
        <div class="search-container">
            <input type="text" id="searchBox" class="form-control" placeholder="Search for a product...">
            <div id="suggestions" class="list-group mt-2"></div>
        </div>
        <div id="productResults" class="mt-4"></div>
    </div>
    
    <script>
        $(document).ready(function() {
            let productData = [];

            // Load product data
            $.getJSON("products.json", function(data) {
                productData = data;
            });

            // Handle input event
            $("#searchBox").on("input", function() {
                let query = $(this).val().toLowerCase();
                let matches = productData.filter(p => p.product_name.toLowerCase().includes(query));
                $("#suggestions").empty();

                matches.slice(0, 5).forEach(m => {
                    $("#suggestions").append(`<button class='list-group-item list-group-item-action' onclick='showProduct("${m.product_name}")'>${m.product_name}</button>`);
                });
            });

            // Handle Enter key
            $("#searchBox").on("keypress", function(event) {
                if (event.which === 13) {
                    let query = $(this).val().toLowerCase();
                    let product = productData.find(p => p.product_name.toLowerCase() === query);
                    if (product) showProduct(product.product_name);
                }
            });

            // Show product details
            window.showProduct = function(name) {
                let product = productData.find(p => p.product_name === name);
                if (product) {
                    let ecoScore = Math.round((product.material_score * 0.4 + (10 - product.carbon_footprint) * 0.5 + product.packaging * 0.1));

                    let tip = "";
                    if (ecoScore >= 8) tip = "🌍 Great choice! This product is highly sustainable.";
                    else if (ecoScore >= 5) tip = "♻️ Decent option, but consider eco-certified alternatives.";
                    else tip = "⚠️ High environmental impact! Look for greener options.";

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

