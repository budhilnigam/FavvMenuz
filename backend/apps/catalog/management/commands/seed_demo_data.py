import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.catalog.models import Restaurant, MenuItem

# Fixed anchor coordinates for synthetic Noida localities
LOCALITY_COORDINATES = {
    'Sector 18': (28.5708, 77.3261),
    'Sector 62': (28.6280, 77.3649),
    'Sector 137': (28.5085, 77.4055),
    'Sector 50': (28.5790, 77.3620),
    'Sector 76': (28.5600, 77.3820),
    'Noida Expressway': (28.5200, 77.3800),
    'Sector 104': (28.5440, 77.3480),
    'Greater Noida West': (28.6010, 77.4350),
}

# 50 Curated Fictional Restaurants
RESTAURANT_DEFINITIONS = [
    # Sector 18 (Entertainment & Dining Hub)
    {"name": "The Tandoor Pavilion", "locality": "Sector 18", "cuisines": ["North Indian", "Mughlai"], "price_band": "₹₹₹", "rating": 4.6, "img": "rest_tandoor"},
    {"name": "Spice Trail Express", "locality": "Sector 18", "cuisines": ["North Indian", "Street Food"], "price_band": "₹₹", "rating": 4.3, "img": "rest_spice"},
    {"name": "Dragon Wok Lounge", "locality": "Sector 18", "cuisines": ["Chinese", "Pan-Asian"], "price_band": "₹₹", "rating": 4.4, "img": "rest_asian"},
    {"name": "Dakshin Vihar", "locality": "Sector 18", "cuisines": ["South Indian"], "price_band": "₹", "rating": 4.5, "img": "rest_south"},
    {"name": "Café Bella Vista", "locality": "Sector 18", "cuisines": ["Italian", "Continental"], "price_band": "₹₹₹", "rating": 4.7, "img": "rest_cafe"},
    {"name": "Sweet Tooth Confectionery", "locality": "Sector 18", "cuisines": ["Desserts", "Bakery"], "price_band": "₹₹", "rating": 4.8, "img": "rest_dessert"},
    {"name": "Urban Greens Salad Bar", "locality": "Sector 18", "cuisines": ["Healthy", "Continental"], "price_band": "₹₹", "rating": 4.2, "img": "rest_healthy"},

    # Sector 62 (Corporate & College Sector)
    {"name": "The Silicon Thali", "locality": "Sector 62", "cuisines": ["North Indian", "Pure Vegetarian"], "price_band": "₹", "rating": 4.3, "img": "rest_thali"},
    {"name": "Lotus Blossom Bistro", "locality": "Sector 62", "cuisines": ["Chinese", "Pan-Asian"], "price_band": "₹₹", "rating": 4.1, "img": "rest_asian"},
    {"name": "Madras Curry Kitchen", "locality": "Sector 62", "cuisines": ["South Indian"], "price_band": "₹", "rating": 4.6, "img": "rest_south"},
    {"name": "Rustic Crust Pizzeria", "locality": "Sector 62", "cuisines": ["Italian"], "price_band": "₹₹", "rating": 4.4, "img": "rest_pizza"},
    {"name": "Chaat Gali Darbar", "locality": "Sector 62", "cuisines": ["Street Food"], "price_band": "₹", "rating": 4.5, "img": "rest_chaat"},
    {"name": "Dhaba 62", "locality": "Sector 62", "cuisines": ["North Indian", "Punjabi"], "price_band": "₹₹", "rating": 4.2, "img": "rest_dhaba"},

    # Sector 137 (Residential High-Rises)
    {"name": "Amaltas Fine Dining", "locality": "Sector 137", "cuisines": ["North Indian", "Mughlai"], "price_band": "₹₹₹", "rating": 4.7, "img": "rest_tandoor"},
    {"name": "Noodle Nest", "locality": "Sector 137", "cuisines": ["Chinese", "Thai"], "price_band": "₹₹", "rating": 4.3, "img": "rest_asian"},
    {"name": "Sattvik Rasoi (Pure Jain)", "locality": "Sector 137", "cuisines": ["North Indian", "Pure Vegetarian"], "price_band": "₹₹", "rating": 4.8, "img": "rest_jain"},
    {"name": "The Espresso & Crumb", "locality": "Sector 137", "cuisines": ["Bakery", "Continental"], "price_band": "₹₹", "rating": 4.5, "img": "rest_cafe"},
    {"name": "Saffron & Pepper", "locality": "Sector 137", "cuisines": ["South Indian", "Coastal"], "price_band": "₹₹", "rating": 4.4, "img": "rest_south"},
    {"name": "Smoky Skewers Grill", "locality": "Sector 137", "cuisines": ["North Indian", "Barbecue"], "price_band": "₹₹₹", "rating": 4.6, "img": "rest_spice"},

    # Sector 50 (Central Residential)
    {"name": "Moti Kebab Terrace", "locality": "Sector 50", "cuisines": ["Mughlai", "North Indian"], "price_band": "₹₹", "rating": 4.5, "img": "rest_tandoor"},
    {"name": "Golden Dragon Dim Sum", "locality": "Sector 50", "cuisines": ["Chinese"], "price_band": "₹₹", "rating": 4.2, "img": "rest_asian"},
    {"name": "Aromas of Mysore", "locality": "Sector 50", "cuisines": ["South Indian"], "price_band": "₹", "rating": 4.7, "img": "rest_south"},
    {"name": "Flour & Stone Trattoria", "locality": "Sector 50", "cuisines": ["Italian"], "price_band": "₹₹₹", "rating": 4.6, "img": "rest_cafe"},
    {"name": "Bikaneri Chaat Kendra", "locality": "Sector 50", "cuisines": ["Street Food", "Desserts"], "price_band": "₹", "rating": 4.4, "img": "rest_chaat"},
    {"name": "Pure Vitality Bowls", "locality": "Sector 50", "cuisines": ["Healthy"], "price_band": "₹₹", "rating": 4.3, "img": "rest_healthy"},

    # Sector 76
    {"name": "Copper Pot Handi", "locality": "Sector 76", "cuisines": ["North Indian"], "price_band": "₹₹", "rating": 4.3, "img": "rest_dhaba"},
    {"name": "Red Lantern Wok", "locality": "Sector 76", "cuisines": ["Chinese", "Pan-Asian"], "price_band": "₹₹", "rating": 4.1, "img": "rest_asian"},
    {"name": "Udupi Sri Krishna Bhavan", "locality": "Sector 76", "cuisines": ["South Indian", "Pure Vegetarian"], "price_band": "₹", "rating": 4.7, "img": "rest_south"},
    {"name": "Oven Story Woodcraft", "locality": "Sector 76", "cuisines": ["Italian", "Fast Food"], "price_band": "₹₹", "rating": 4.0, "img": "rest_pizza"},
    {"name": "ChocoLush Patisserie", "locality": "Sector 76", "cuisines": ["Desserts", "Bakery"], "price_band": "₹₹", "rating": 4.8, "img": "rest_dessert"},
    {"name": "The Dosa Corner", "locality": "Sector 76", "cuisines": ["South Indian", "Street Food"], "price_band": "₹", "rating": 4.5, "img": "rest_south"},

    # Noida Expressway
    {"name": "Grand Royal Horizon", "locality": "Noida Expressway", "cuisines": ["North Indian", "Continental"], "price_band": "₹₹₹₹", "rating": 4.9, "img": "rest_fine"},
    {"name": "Silk Route Dum Pukht", "locality": "Noida Expressway", "cuisines": ["Mughlai", "Awadhi"], "price_band": "₹₹₹", "rating": 4.8, "img": "rest_tandoor"},
    {"name": "Sakura Japanese & Asian", "locality": "Noida Expressway", "cuisines": ["Pan-Asian", "Japanese"], "price_band": "₹₹₹₹", "rating": 4.7, "img": "rest_asian"},
    {"name": "The Mediterranean Shore", "locality": "Noida Expressway", "cuisines": ["Continental", "Italian"], "price_band": "₹₹₹", "rating": 4.6, "img": "rest_cafe"},
    {"name": "Express Highway Dhaba", "locality": "Noida Expressway", "cuisines": ["North Indian", "Punjabi"], "price_band": "₹", "rating": 4.2, "img": "rest_dhaba"},
    {"name": "Zenith Cloud Lounge", "locality": "Noida Expressway", "cuisines": ["Continental", "Finger Food"], "price_band": "₹₹₹", "rating": 4.4, "img": "rest_cafe"},

    # Sector 104 (Trendy Food Boulevard)
    {"name": "Artisan Bread & Brew", "locality": "Sector 104", "cuisines": ["Continental", "Bakery"], "price_band": "₹₹₹", "rating": 4.7, "img": "rest_cafe"},
    {"name": "Tiki Taco & Grill", "locality": "Sector 104", "cuisines": ["Mexican", "Continental"], "price_band": "₹₹", "rating": 4.4, "img": "rest_cafe"},
    {"name": "Baozi Asian House", "locality": "Sector 104", "cuisines": ["Pan-Asian", "Chinese"], "price_band": "₹₹", "rating": 4.6, "img": "rest_asian"},
    {"name": "Kathiawadi Rasoi", "locality": "Sector 104", "cuisines": ["Gujarati", "Pure Vegetarian"], "price_band": "₹₹", "rating": 4.5, "img": "rest_jain"},
    {"name": "Napoli Fire Crust", "locality": "Sector 104", "cuisines": ["Italian"], "price_band": "₹₹₹", "rating": 4.8, "img": "rest_pizza"},
    {"name": "Kulfi & Falooda Junction", "locality": "Sector 104", "cuisines": ["Desserts"], "price_band": "₹", "rating": 4.6, "img": "rest_dessert"},
    {"name": "Punjab Grillworks", "locality": "Sector 104", "cuisines": ["North Indian", "Mughlai"], "price_band": "₹₹₹", "rating": 4.5, "img": "rest_tandoor"},

    # Greater Noida West (Rapid Growth Corridor)
    {"name": "Kaveri Vegetarian Treat", "locality": "Greater Noida West", "cuisines": ["South Indian", "North Indian"], "price_band": "₹", "rating": 4.3, "img": "rest_thali"},
    {"name": "Wok On Fire", "locality": "Greater Noida West", "cuisines": ["Chinese"], "price_band": "₹", "rating": 4.1, "img": "rest_asian"},
    {"name": "Pind Punjabi Tadka", "locality": "Greater Noida West", "cuisines": ["North Indian", "Punjabi"], "price_band": "₹₹", "rating": 4.4, "img": "rest_dhaba"},
    {"name": "Chettinad Leaf", "locality": "Greater Noida West", "cuisines": ["South Indian"], "price_band": "₹₹", "rating": 4.5, "img": "rest_south"},
    {"name": "Crust & Craft Pizza", "locality": "Greater Noida West", "cuisines": ["Italian", "Fast Food"], "price_band": "₹₹", "rating": 4.2, "img": "rest_pizza"},
    {"name": "Heritage Sweets & Snacks", "locality": "Greater Noida West", "cuisines": ["Street Food", "Desserts"], "price_band": "₹", "rating": 4.6, "img": "rest_chaat"},
]

# Cuisine Dish Catalog Generator
CUISINE_DISH_TEMPLATES = {
    "North Indian": [
        {"name": "Tandoori Paneer Tikka", "cat": "Starters", "desc": "Cottage cheese cubes marinated in spiced hung yogurt and grilled over smoky charcoal.", "price": 320, "ingredients": ["paneer", "yogurt", "capsicum", "onion", "garam masala"], "tags": ["vegetarian", "gluten_free"], "spice": "spicy", "allergens": ["dairy"]},
        {"name": "Jain Paneer Tikka (Zero Onion Garlic)", "cat": "Starters", "desc": "Grilled cottage cheese cubes in spiced carom-seed yogurt marinade, strictly no root vegetables.", "price": 340, "ingredients": ["paneer", "curd", "capsicum", "carom seeds", "coriander"], "tags": ["vegetarian", "jain_friendly", "gluten_free"], "spice": "medium", "allergens": ["dairy"]},
        {"name": "Dal Makhani Slow Cooked", "cat": "Main Course", "desc": "Black lentils simmered overnight with fresh cream, ripe tomatoes, and homemade white butter.", "price": 280, "ingredients": ["black lentils", "kidney beans", "butter", "cream", "tomatoes"], "tags": ["vegetarian", "gluten_free"], "spice": "mild", "allergens": ["dairy"]},
        {"name": "Peshawari Paneer Butter Masala", "cat": "Main Course", "desc": "Soft paneer cubes simmered in a velvety cashew and tomato gravy with aromatic fenugreek.", "price": 350, "ingredients": ["paneer", "cashew paste", "tomatoes", "butter", "fenugreek"], "tags": ["vegetarian"], "spice": "medium", "allergens": ["dairy", "nuts"]},
        {"name": "Palak Corn Melange", "cat": "Main Course", "desc": "Fresh spinach puree tempered with roasted cumin, tender sweet corn, and mild garlic cloves.", "price": 290, "ingredients": ["spinach", "sweet corn", "garlic", "cumin", "green chillies"], "tags": ["vegetarian", "vegan", "dairy_free", "gluten_free"], "spice": "mild", "allergens": []},
        {"name": "Jain Yellow Dal Tadka", "cat": "Main Course", "desc": "Yellow toor dal tempered with cumin, green chillies, and asafoetida. Prepared without onion and garlic.", "price": 220, "ingredients": ["toor dal", "cumin", "asafoetida", "green chillies", "ghee"], "tags": ["vegetarian", "jain_friendly", "gluten_free"], "spice": "medium", "allergens": ["dairy"]},
        {"name": "Amritsari Kulcha with Chole", "cat": "Main Course", "desc": "Crispy layered stuffed flatbread served with tangy chickpeas and pickled onions.", "price": 240, "ingredients": ["flour", "potatoes", "chickpeas", "coriander", "anardana"], "tags": ["vegetarian", "vegan", "dairy_free"], "spice": "spicy", "allergens": ["gluten"]},
        {"name": "Garlic Butter Naan", "cat": "Breads", "desc": "Clay-oven baked leavened flatbread brushed with crushed garlic and melted butter.", "price": 75, "ingredients": ["flour", "garlic", "butter", "coriander"], "tags": ["vegetarian"], "spice": "mild", "allergens": ["gluten", "dairy"]},
        {"name": "Tandoori Roti (Whole Wheat)", "cat": "Breads", "desc": "Crisp whole wheat bread roasted in clay tandoor.", "price": 35, "ingredients": ["whole wheat flour", "water"], "tags": ["vegetarian", "vegan", "jain_friendly", "dairy_free"], "spice": "none", "allergens": ["gluten"]},
        {"name": "Subz Dum Biryani", "cat": "Biryani & Rice", "desc": "Long-grain basmati rice layered with garden vegetables, saffron milk, and aromatic whole spices.", "price": 360, "ingredients": ["basmati rice", "beans", "carrots", "cauliflower", "saffron", "cardamom"], "tags": ["vegetarian", "gluten_free"], "spice": "spicy", "allergens": ["dairy"]},
        {"name": "Jeera Rice", "cat": "Biryani & Rice", "desc": "Fragrant basmati rice gently tempered with roasted cumin seeds and fresh coriander.", "price": 180, "ingredients": ["basmati rice", "cumin seeds", "ghee", "coriander"], "tags": ["vegetarian", "jain_friendly", "gluten_free"], "spice": "none", "allergens": ["dairy"]},
    ],
    "South Indian": [
        {"name": "Ghee Roast Masala Dosa", "cat": "Dosa Specials", "desc": "Paper-thin fermented rice crepe crisped with pure golden desi ghee, stuffed with seasoned spiced potato filling.", "price": 190, "ingredients": ["rice", "urad dal", "desi ghee", "potatoes", "mustard seeds"], "tags": ["vegetarian", "gluten_free"], "spice": "medium", "allergens": ["dairy"]},
        {"name": "Mysore Onion Rava Masala Dosa", "cat": "Dosa Specials", "desc": "Semolina batter crepe roasted with spicy red chili chutney, crunchy onions, and cilantro.", "price": 220, "ingredients": ["semolina", "rice flour", "onions", "red chili paste", "curry leaves"], "tags": ["vegetarian", "vegan", "dairy_free"], "spice": "spicy", "allergens": ["gluten"]},
        {"name": "Jain Plain Ghee Dosa", "cat": "Dosa Specials", "desc": "Crispy golden fermented crepe cooked in pure ghee, accompanied by fresh coconut chutney and Jain sambar.", "price": 170, "ingredients": ["rice", "urad dal", "desi ghee", "coconut", "mustard seeds"], "tags": ["vegetarian", "jain_friendly", "gluten_free"], "spice": "mild", "allergens": ["dairy"]},
        {"name": "Steamed Button Idli Sambar (10 pcs)", "cat": "Tiffin", "desc": "Pillowy soft fermented rice cakes served immersed in hot tangy vegetable lentil stew.", "price": 140, "ingredients": ["rice", "urad dal", "toor dal", "drumsticks", "tamarind"], "tags": ["vegetarian", "vegan", "dairy_free", "gluten_free"], "spice": "mild", "allergens": []},
        {"name": "Crispy Medu Vada (2 pcs)", "cat": "Tiffin", "desc": "Golden fried lentil donuts infused with crushed black pepper, fresh ginger, and curry leaves.", "price": 130, "ingredients": ["urad dal", "black pepper", "curry leaves", "ginger", "asafoetida"], "tags": ["vegetarian", "vegan", "dairy_free", "gluten_free"], "spice": "medium", "allergens": []},
        {"name": "Podi Onion Tomato Uttapam", "cat": "Tiffin", "desc": "Thick sourdough pancake topped with caramelized shallots, juicy tomatoes, and fiery gunpowder spice.", "price": 210, "ingredients": ["rice batter", "shallots", "tomatoes", "gunpowder podi", "sesame oil"], "tags": ["vegetarian", "vegan", "dairy_free", "gluten_free"], "spice": "spicy", "allergens": ["sesame"]},
        {"name": "Traditional Curd Rice", "cat": "Rice Bowls", "desc": "Comforting cooked rice folded into seasoned fresh yogurt, tempered with curry leaves, mustard seeds, and pomegranate seeds.", "price": 160, "ingredients": ["rice", "yogurt", "mustard seeds", "curry leaves", "pomegranate"], "tags": ["vegetarian", "jain_friendly", "gluten_free"], "spice": "mild", "allergens": ["dairy"]},
        {"name": "South Indian Filter Coffee", "cat": "Beverages", "desc": "Slow-brewed dark chicory blend frothed high with hot whole milk.", "price": 70, "ingredients": ["coffee decoction", "chicory", "milk", "sugar"], "tags": ["vegetarian", "jain_friendly", "gluten_free"], "spice": "none", "allergens": ["dairy"]},
    ],
    "Chinese": [
        {"name": "Crispy Chilli Paneer Dry", "cat": "Starters", "desc": "Wok-tossed battered cottage cheese tossed with bell peppers, green chillies, garlic, and light soy sauce.", "price": 310, "ingredients": ["paneer", "bell peppers", "garlic", "green chillies", "soy sauce"], "tags": ["vegetarian"], "spice": "spicy", "allergens": ["dairy", "soy", "gluten"]},
        {"name": "Veg Spring Rolls with Sweet Chilli Dip", "cat": "Starters", "desc": "Golden fried crispy pastry rolls packed with julienned cabbage, carrots, and glass noodles.", "price": 240, "ingredients": ["cabbage", "carrots", "flour pastry", "glass noodles", "white pepper"], "tags": ["vegetarian", "vegan", "dairy_free"], "spice": "mild", "allergens": ["gluten"]},
        {"name": "Steamed Veg Dim Sum (6 pcs)", "cat": "Dim Sums", "desc": "Translucent dumplings stuffed with finely minced water chestnuts, shiitake mushrooms, and bok choy.", "price": 280, "ingredients": ["water chestnuts", "mushrooms", "bok choy", "sesame oil", "potato starch"], "tags": ["vegetarian", "vegan", "dairy_free", "gluten_free"], "spice": "mild", "allergens": ["sesame"]},
        {"name": "Spicy Schezwan Hakka Noodles", "cat": "Noodles & Rice", "desc": "Wheat noodles wok-fried at high heat with shredded crisp vegetables in fiery homemade red chili Schezwan sauce.", "price": 260, "ingredients": ["noodles", "bell peppers", "cabbage", "schezwan peppers", "garlic"], "tags": ["vegetarian", "vegan", "dairy_free"], "spice": "extra_spicy", "allergens": ["gluten", "soy"]},
        {"name": "Burnt Garlic Veg Fried Rice", "cat": "Noodles & Rice", "desc": "Fragrant long grain rice stir-fried with golden toasted garlic chips, spring onions, and carrots.", "price": 250, "ingredients": ["rice", "burnt garlic", "spring onions", "carrots", "soy sauce"], "tags": ["vegetarian", "vegan", "dairy_free"], "spice": "medium", "allergens": ["soy"]},
        {"name": "Veg Manchurian in Hot Garlic Gravy", "cat": "Main Course", "desc": "Minced vegetable orbs simmered in a luscious dark soya, coriander, and hot garlic broth.", "price": 290, "ingredients": ["cauliflower", "cabbage", "garlic", "soya sauce", "green chillies"], "tags": ["vegetarian", "vegan", "dairy_free"], "spice": "spicy", "allergens": ["soy", "gluten"]},
        {"name": "Hot & Sour Vegetable Soup", "cat": "Soups", "desc": "Classic tangy and peppery broth loaded with shredded bamboo shoots, tofu, and black fungus mushrooms.", "price": 180, "ingredients": ["tofu", "mushrooms", "white pepper", "dark vinegar", "soy sauce"], "tags": ["vegetarian", "vegan", "dairy_free", "gluten_free"], "spice": "spicy", "allergens": ["soy"]},
    ],
    "Italian": [
        {"name": "Classic Woodfired Margherita Pizza", "cat": "Pizzas", "desc": "San Marzano plum tomato sauce, fresh buffalo mozzarella, fragrant sweet basil, and extra virgin olive oil.", "price": 450, "ingredients": ["flour", "tomato sauce", "mozzarella", "fresh basil", "olive oil"], "tags": ["vegetarian"], "spice": "mild", "allergens": ["gluten", "dairy"]},
        {"name": "Quattro Formaggi Pizza (Jain Option)", "cat": "Pizzas", "desc": "Hand-stretched sourdough pizza topped with mozzarella, parmesan, gorgonzola, and ricotta with oregano.", "price": 540, "ingredients": ["flour", "mozzarella", "parmesan", "ricotta", "gorgonzola", "oregano"], "tags": ["vegetarian", "jain_friendly"], "spice": "mild", "allergens": ["gluten", "dairy"]},
        {"name": "Penne all'Arrabbiata", "cat": "Pasta", "desc": "Al dente penne pasta tossed in a fiery crushed plum tomato, garlic, and red chili flake sauce with fresh parsley.", "price": 380, "ingredients": ["penne", "tomatoes", "garlic", "chili flakes", "parsley", "olive oil"], "tags": ["vegetarian", "vegan", "dairy_free"], "spice": "spicy", "allergens": ["gluten"]},
        {"name": "Creamy Fettuccine Alfredo con Funghi", "cat": "Pasta", "desc": "Ribbon pasta coated in rich parmesan butter cream sauce with sauteed wild portobello mushrooms.", "price": 420, "ingredients": ["fettuccine", "parmesan cheese", "heavy cream", "portobello mushrooms", "butter"], "tags": ["vegetarian"], "spice": "mild", "allergens": ["gluten", "dairy"]},
        {"name": "Artisanal Herb Garlic Bread", "cat": "Starters", "desc": "Toasted rustic ciabatta slices infused with roasted garlic butter, rosemary, and thyme.", "price": 190, "ingredients": ["ciabatta bread", "garlic", "butter", "rosemary", "sea salt"], "tags": ["vegetarian"], "spice": "mild", "allergens": ["gluten", "dairy"]},
        {"name": "Tiramisu della Nonna", "cat": "Desserts", "desc": "Espresso-soaked savoiardi ladyfingers layered with whipped mascarpone cream and dusted with bitter Dutch cocoa.", "price": 280, "ingredients": ["mascarpone", "espresso coffee", "savoiardi biscuits", "cocoa powder"], "tags": ["vegetarian"], "spice": "none", "allergens": ["dairy", "gluten"]},
    ],
    "Street Food": [
        {"name": "Delhi Special Dahi Bhalla Chaat", "cat": "Chaat Counter", "desc": "Lentil fritters soaked in spiced curd, topped with saunth sonth dates chutney, mint chutney, and roasted cumin.", "price": 150, "ingredients": ["urad dal", "sweet curd", "tamarind chutney", "mint chutney", "cumin"], "tags": ["vegetarian", "gluten_free"], "spice": "medium", "allergens": ["dairy"]},
        {"name": "Crispy Aloo Tikki Chole", "cat": "Chaat Counter", "desc": "Pan-fried crisp potato patties served with spiced chickpea curry, chopped onions, and zesty lemon drizzle.", "price": 140, "ingredients": ["potatoes", "chickpeas", "coriander", "green chillies", "onions"], "tags": ["vegetarian", "vegan", "dairy_free"], "spice": "spicy", "allergens": []},
        {"name": "Kolkata Puchka & Pani Puri Platter", "cat": "Chaat Counter", "desc": "Eight hollow crispy semolina puris served with spicy mint-coriander water and spiced potato stuffing.", "price": 90, "ingredients": ["semolina puris", "mint water", "tamarind water", "potatoes", "black salt"], "tags": ["vegetarian", "vegan", "dairy_free"], "spice": "extra_spicy", "allergens": ["gluten"]},
        {"name": "Mumbai Pav Bhaji with Extra Butter", "cat": "Street Classics", "desc": "Slow-mashed spiced vegetable medley served with two piping hot butter-toasted pav buns.", "price": 190, "ingredients": ["potatoes", "tomatoes", "capsicum", "pav buns", "butter", "pav bhaji masala"], "tags": ["vegetarian"], "spice": "spicy", "allergens": ["gluten", "dairy"]},
        {"name": "Jain Sev Puri", "cat": "Chaat Counter", "desc": "Flat crisps loaded with raw banana mash, sweet date chutney, and heaps of crispy chickpea sev.", "price": 120, "ingredients": ["flour papdi", "raw banana", "tamarind chutney", "sev", "coriander"], "tags": ["vegetarian", "vegan", "jain_friendly", "dairy_free"], "spice": "medium", "allergens": ["gluten"]},
    ],
    "Healthy": [
        {"name": "Mediterranean Falafel Hummus Bowl", "cat": "Power Bowls", "desc": "Crisp herb falafels, smoked paprika hummus, cucumber tomato salad, kalamata olives, and warm pita wedges.", "price": 360, "ingredients": ["chickpeas", "tahini", "cucumber", "olives", "pita bread", "parsley"], "tags": ["vegetarian", "vegan", "dairy_free"], "spice": "mild", "allergens": ["gluten", "sesame"]},
        {"name": "Avocado & Quinoa Protein Salad", "cat": "Salads", "desc": "Organic tri-color quinoa, Hass avocado slices, cherry tomatoes, and toasted pumpkin seeds with lemon vinaigrette.", "price": 390, "ingredients": ["quinoa", "avocado", "cherry tomatoes", "pumpkin seeds", "lemon olive oil"], "tags": ["vegetarian", "vegan", "jain_friendly", "dairy_free", "gluten_free"], "spice": "mild", "allergens": []},
        {"name": "Tofu & Edamame Soba Noodle Bowl", "cat": "Power Bowls", "desc": "Buckwheat soba noodles, pan-seared sesame tofu, edamame beans, and baby spinach in ginger soy glaze.", "price": 380, "ingredients": ["soba noodles", "organic tofu", "edamame", "sesame seeds", "ginger"], "tags": ["vegetarian", "vegan", "dairy_free"], "spice": "mild", "allergens": ["soy", "sesame", "gluten"]},
        {"name": "Cold Pressed Green Detox Juice", "cat": "Cold Pressed", "desc": "Pure cold-pressed cucumber, green apple, celery, baby spinach, and fresh ginger. No added sugar.", "price": 160, "ingredients": ["cucumber", "green apple", "celery", "spinach", "ginger"], "tags": ["vegetarian", "vegan", "jain_friendly", "dairy_free", "gluten_free"], "spice": "none", "allergens": []},
    ],
    "Desserts": [
        {"name": "Hot Gulab Jamun (2 pcs)", "cat": "Warm Desserts", "desc": "Soft khoya milk dumplings fried to golden brown and steeped in green cardamom and rose sugar syrup.", "price": 110, "ingredients": ["khoya milk solids", "flour", "sugar syrup", "cardamom", "rose water"], "tags": ["vegetarian"], "spice": "none", "allergens": ["dairy", "gluten"]},
        {"name": "Kesar Pista Rasmalai", "cat": "Chilled Sweets", "desc": "Tender poached cottage cheese discs steeped in saffron infused rabri with crushed pistachios.", "price": 140, "ingredients": ["paneer chhena", "milk rabri", "saffron", "pistachios", "cardamom"], "tags": ["vegetarian", "jain_friendly", "gluten_free"], "spice": "none", "allergens": ["dairy", "nuts"]},
        {"name": "Gooey Belgian Dark Chocolate Brownie", "cat": "Bakes", "desc": "Warm 70% dark chocolate fudge brownie topped with roasted walnuts and chocolate ganache.", "price": 180, "ingredients": ["belgian dark chocolate", "butter", "flour", "walnuts", "cocoa"], "tags": ["vegetarian"], "spice": "none", "allergens": ["dairy", "gluten", "nuts"]},
        {"name": "Kesar Matka Kulfi", "cat": "Ice Creams", "desc": "Traditional slow-reduced dense milk ice cream flavored with saffron threads and sliced almonds.", "price": 120, "ingredients": ["whole milk", "saffron", "almonds", "cardamom"], "tags": ["vegetarian", "jain_friendly", "gluten_free"], "spice": "none", "allergens": ["dairy", "nuts"]},
    ],
    "Beverages": [
        {"name": "Royal Masala Chai", "cat": "Beverages", "desc": "Assam black tea brewed with fresh ginger, green cardamom, cloves, and whole milk.", "price": 60, "ingredients": ["tea leaves", "milk", "ginger", "cardamom"], "tags": ["vegetarian", "jain_friendly", "gluten_free"], "spice": "mild", "allergens": ["dairy"]},
        {"name": "Thandi Punjabi Sweet Lassi", "cat": "Beverages", "desc": "Thick churned sweet yogurt drink topped with a dollop of fresh clotted cream and pistachios.", "price": 120, "ingredients": ["curd", "sugar", "pistachios", "rose water"], "tags": ["vegetarian", "jain_friendly", "gluten_free"], "spice": "none", "allergens": ["dairy", "nuts"]},
        {"name": "Fresh Lime Soda (Sweet & Salted)", "cat": "Beverages", "desc": "Sparkling soda with freshly squeezed Key limes, rock salt, and mint leaves.", "price": 90, "ingredients": ["soda", "lime juice", "mint", "rock salt"], "tags": ["vegetarian", "vegan", "jain_friendly", "dairy_free", "gluten_free"], "spice": "none", "allergens": []},
        {"name": "Alphonso Mango Shake", "cat": "Beverages", "desc": "Rich blend of pure Alphonso mango pulp, chilled milk, and vanilla drizzle.", "price": 150, "ingredients": ["mango pulp", "milk", "sugar"], "tags": ["vegetarian", "jain_friendly", "gluten_free"], "spice": "none", "allergens": ["dairy"]},
    ]
}


class Command(BaseCommand):
    help = "Seeds deterministic synthetic demo restaurants and menu items in Noida localities."

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Destructively delete all existing demo records before seeding.',
        )

    def handle(self, *args, **options):
        # Enforce deterministic random seed
        random.seed(42)

        reset = options.get('reset', False)
        if reset:
            self.stdout.write(self.style.WARNING("Reset requested. Deleting existing demo data..."))
            deleted_items, _ = MenuItem.objects.filter(is_demo=True).delete()
            deleted_rests, _ = Restaurant.objects.filter(is_demo=True).delete()
            self.stdout.write(f"Deleted {deleted_rests} demo restaurants and {deleted_items} demo menu items.")

        self.stdout.write(self.style.MIGRATE_HEADING("Seeding synthetic restaurant and menu catalog..."))

        total_restaurants_created = 0
        total_items_created = 0

        for idx, rest_def in enumerate(RESTAURANT_DEFINITIONS, start=1):
            locality = rest_def["locality"]
            base_lat, base_lng = LOCALITY_COORDINATES.get(locality, (28.5355, 77.3910))

            # Add small deterministic jitter (±0.005 deg ~ 500m)
            jitter_lat = ((idx * 7) % 19 - 9) * 0.0006
            jitter_lng = ((idx * 11) % 19 - 9) * 0.0006
            lat = round(base_lat + jitter_lat, 6)
            lng = round(base_lng + jitter_lng, 6)

            name = rest_def["name"]
            slug = slugify(name)

            restaurant, created = Restaurant.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "description": f"A delightful dining destination in {locality} known for authentic {', '.join(rest_def['cuisines'])} offerings.",
                    "cuisines": rest_def["cuisines"],
                    "locality": locality,
                    "address": f"Shop {10 + (idx % 40)}, Central Commercial Galleria, {locality}, Noida, UP",
                    "latitude": lat,
                    "longitude": lng,
                    "price_band": rest_def["price_band"],
                    "rating": rest_def["rating"],
                    "review_count": 80 + (idx * 13) % 400,
                    "image_asset": rest_def.get("img", "rest_default"),
                    "is_demo": True,
                }
            )

            if created:
                total_restaurants_created += 1

            # Decide which dish categories belong to this restaurant based on its cuisines
            dishes_for_restaurant = []
            for cuisine in rest_def["cuisines"]:
                matched_category = None
                for cat_key in CUISINE_DISH_TEMPLATES:
                    if cat_key.lower() in cuisine.lower():
                        matched_category = cat_key
                        break
                if matched_category:
                    dishes_for_restaurant.extend(CUISINE_DISH_TEMPLATES[matched_category])

            # Always add desserts and beverages to make each menu rich and realistic
            dishes_for_restaurant.extend(CUISINE_DISH_TEMPLATES["Desserts"][:3])
            dishes_for_restaurant.extend(CUISINE_DISH_TEMPLATES["Beverages"][:3])

            # Deduplicate by dish name
            unique_dishes = {d["name"]: d for d in dishes_for_restaurant}.values()

            # Seed menu items for this restaurant
            for dish in unique_dishes:
                item_slug = f"{slug}-{slugify(dish['name'])}"
                price_paise = int(dish["price"] * 100)

                _, item_created = MenuItem.objects.get_or_create(
                    restaurant=restaurant,
                    slug=item_slug,
                    defaults={
                        "name": dish["name"],
                        "category": dish["cat"],
                        "description": dish["desc"],
                        "price_paise": price_paise,
                        "ingredients": dish["ingredients"],
                        "dietary_tags": dish["tags"],
                        "spice_level": dish["spice"],
                        "allergen_info": dish["allergens"],
                        "image_asset": "dish_default",
                        "is_available": True,
                        "is_demo": True,
                    }
                )
                if item_created:
                    total_items_created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded catalog! Created {total_restaurants_created} restaurants "
            f"and {total_items_created} menu items. Total demo restaurants now: {Restaurant.objects.filter(is_demo=True).count()}, "
            f"Total demo menu items: {MenuItem.objects.filter(is_demo=True).count()}."
        ))
