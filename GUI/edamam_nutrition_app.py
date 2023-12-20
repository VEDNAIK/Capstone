import streamlit as st
import requests
import configparser

# Read credentials from the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

app_id = config['Edamam']['app_id']
app_key = config['Edamam']['app_key']

def get_nutritional_info(ingredients):
    api_url = f'https://api.edamam.com/api/nutrition-data'
    nutritional_data = []

    for ingredient in ingredients:
        params = {
            'app_id': app_id,
            'app_key': app_key,
            'ingr': ingredient
        }
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            nutritional_data.append(data)
        else:
            st.error(f"API request failed with status code {response.status_code}")
    
    return nutritional_data

# Create the Streamlit app.
st.title('Nutritional Analysis App')
user_input = st.text_area("Enter Ingredients (separated by commas)")

if st.button('Get Nutritional Info'):
    if user_input:
        ingredients_list = [ingredient.strip() for ingredient in user_input.split(',')]
        nutritional_data = get_nutritional_info(ingredients_list)
        if nutritional_data:
            st.write("# Nutritional Analysis:")
            for i, data in enumerate(nutritional_data, start=1):
                st.write(f"## Ingredient {i}:")
                st.write(f"**Calories**: {data['calories']} kcal")
                st.write(f"**Total Weight**: {data['totalWeight']} g")
                st.write("## Diet Labels:")
                st.write(", ".join(data['dietLabels']))
                st.write("## Health Labels:")
                st.write(", ".join(data['healthLabels']))
                st.write("## Total Nutrients:")
                st.write("```")
                for nutrient, info in data['totalNutrients'].items():
                    st.write(f"{info['label']}: {info['quantity']} {info['unit']}")
                st.write("```")
    else:
        st.warning("Please enter the ingredients.")
