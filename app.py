#i will import libraries here - if you dont know what these libraries are, better start learning now itself, as for why i used fuzzy its down below.
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fuzzywuzzy import fuzz # i will use fuzz to help me find products in dataset - here fuzzy will compare our search text to actual product name
from fuzzywuzzy import process # process is used to return the best match for searched product.

# Load the dataset nothing complex here, i will instead use a function to make it more pleasing, looks professional and for convenience ofcourse.
def load_data():
    file_path = "eco_friendly_product_cleaned.csv" #csv file is already cleaned - that is devoid of repetitions,and only unique values are present. yeah i checked each personally it sucks.
    df = pd.read_csv(file_path)
    return df

df = load_data() #call function to load csv simple as that.

# for anyone who doesnt understand whats st? below, its short alias for streamlit,instead of writting streamlit.title we can simply use st as short cut, and we can still use same operation.
st.title("\U0001F331 Eco-Friendly Shopping Assistant")

st.markdown("## Please select category")

# Category selection - note that since my dataset is already cleaned there is no need for unique() but for procedures, i will include it, just in case there are any repeats
categories = df['Category'].unique().tolist()
selected_category = st.selectbox("Select category", categories) # selectbox will be used for creating dropbox, in case you dont know , most importantly lets you choose things from list instead of entering in case the user is so dumb we have to give a selection drop columm haha.

# Initialize session state for product_name
if "product_name" not in st.session_state:  # whats this session state you ask?? i learnt it before few hours too haha, basically It remembers values across user interactions (e.g., dropdown selections, text inputs).
    st.session_state.product_name = "" #Without st.session_state, Streamlit would reset everything every time the user interacts with something. thats why its important.

# Product search input
product_name = st.text_input("Enter Product Name", value=st.session_state.product_name, key="product_name_input")  #for people out there, text_input is basically input function or should i say its like scanf in c, i hope that makes sense (hopefully

# Product dropdown (Moved Below Text Input)  sad news, this drop below not's working i dont know why but godknows why. i will keep it.
available_products = df[df['Category'] == selected_category]['Product'].unique().tolist()
selected_product = st.selectbox("Available Products", [""] + available_products, key="available_products")

# Sync text input with selected product - here to make sure that selected code appears even in enter product column, it may look like magic but who knew its just updating text lmfao
if selected_product:
    if st.session_state.product_name != selected_product:
        st.session_state.product_name = selected_product  # Update text input - this line is what's causing the updated text input, dang it i love how this works, too bad i dont have much knowledge i only learned basics.
        st.rerun()

# Fuzzy matching for manual entry - this is fuzzy comes in handy. here below you may see "score" this score is actually to see how much input string matches with product in database, and helps to find best match, since there are no repition this works really well since there is one of product with that name haha.
elif product_name:
    best_match, score = process.extractOne(product_name, df['Product'].tolist(), scorer=fuzz.token_sort_ratio)
    if score >= 70:  # Adjust threshold as needed
        st.session_state.product_name = best_match
    else:
        st.session_state.product_name = product_name

# Function to get eco score and tip - originally i didnt wanted to add tip for each product, because just take a look at my dataset it has 1000 entries i am so tired trying to find a suitable tip for each product, on second thought maybe i shouldnt have added tip, god why do i make things harder for myself?? hardest difficulty was finding a suitable tip on my owm, lmao. update after a day of looking i finally somehow managed to enter a tip for each product god dammit.
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

    # Plotting eco-score - this aint me, below code i found this snippet on internet and i modified to match the project elements, dont ask where i got it.
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=int(eco_score) if eco_score.isdigit() else 0,  # Convert score to int if possible
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Selected Product Eco-Score"},
        gauge={'axis': {'range': [None, 5]},
               'bar': {'color': "darkblue"},
               'steps': [
                   {'range': [0, 2], 'color': "lightgreen"},
                   {'range': [2, 3], 'color': "yellow"},
                   {'range': [3, 5], 'color': "red"}]}))
    st.plotly_chart(fig)
