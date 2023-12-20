import streamlit as st
import requests
import json
from PIL import Image
import io
import pandas as pd
import nltk
from nltk import sent_tokenize
import re

# Define the Streamlit app
st.set_page_config(
    page_title="Culinary Curator - Recipe Recommendation System",
    page_icon="🍔",
    layout="wide",
)

# Create a session state to store the uploaded image and predicted name
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "predicted_name" not in st.session_state:
    st.session_state.predicted_name = ""

# Define custom CSS styles
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
        font-family: Arial, sans-serif;
    }
    .stButton > button {
        background-color: #ff6f61;
        color: white;
        font-weight: bold;
        border-radius: 5px;
    }
    .stTextInput {
        background-color: #e1e5eb;
    }
    .stText > p {
        font-style: italic;
    }
    .stImage img {
        border-radius: 10px;
    }
    .stSubheader {
        font-size: 24px;
        font-weight: bold;
        color: #333;
        background-color: #ff6f61;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add a title with a fun background color
st.title("Culinary Curator - Recipe Recommendation System")
st.markdown("<p class='stSubheader'>Discover Delicious Recipes</p>", unsafe_allow_html=True)

# Create an input field for the user to enter ingredients
user_input = st.text_area("Enter ingredients (comma-separated):", st.session_state.predicted_name)

# Create a button to trigger the image upload process
image_upload = st.file_uploader("Upload an image of a fruit or vegetable:", type=["jpg", "png"])

# Create a button to trigger the recommendation process
recommendation_button_key = "recommend_button"
if st.button("Get Recommendations", key=recommendation_button_key):
    if not st.session_state.predicted_name and not user_input:
        st.error("Please upload an image or enter ingredients first.")
    else:
        # Choose either the predicted name from the image or the user's input
        selected_ingredient = st.session_state.predicted_name
        # If the user has entered additional ingredients manually, append them
        if user_input:
            selected_ingredient += f", {user_input}"
        # Send the user input to the backend for recipe recommendations
        data = {"user_input": selected_ingredient}
        response = requests.post("http://localhost:5000/recommend", json=data)
        if response.status_code == 200:
            recommendations = json.loads(response.text)["recommendations"]
            recommendations = pd.DataFrame(recommendations)
            
            st.subheader("Recommended Recipes:")
            
            for i in range(len(recommendations)):
                sentences = sent_tokenize(recommendations["TranslatedInstructions"][i])
                
                st.write(f"Recipe {i+1}:\n")
                st.markdown(f"**{recommendations['TranslatedRecipeName'][i]}**", unsafe_allow_html=True)
                # Display the image from an URL with a fixed width and height
                image_url = recommendations["image-url"][i]  # Replace with the actual URL
                width = 400  # Set the desired width in pixels
                height = 300  # Set the desired height in pixels
                
                st.markdown(f"<img src='{image_url}' width='{width}' height='{height}'>", unsafe_allow_html=True)
                st.write("\n")
                st.write(f"Ingredients: \n")
                recommendations["TranslatedIngredients"][i] = recommendations["TranslatedIngredients"][i].replace(',', ', ')
                st.markdown(recommendations["TranslatedIngredients"][i], unsafe_allow_html=True)
                r = recommendations["TotalTimeInMins"][i]
                st.write(f"Total Time (minutes): {r} \n")
                c= recommendations["Cuisine"][i]
                st.write(f"Cuisine: {c} \n")
                st.markdown(f"Instructions: \n")
                end_punctuations = ['.', '!', '?']
                sentences = []
                sentence = []
                for char in recommendations["TranslatedInstructions"][i]:
                    sentence.append(char)
                    if char in end_punctuations:
                        sentences.append(''.join(sentence))
                        sentence = []
                for s in sentences:
                    st.markdown(s.strip(), unsafe_allow_html=True)
                
                st.markdown(f"Video Instructions: \n")
                st.write(recommendations["URL"][i])
                st.write("\n")

# Check if an image is uploaded
if image_upload is not None:
    # Create a button to trigger the image prediction process
    prediction_button_key = "prediction_button"
    if st.button("Predict Image", key=prediction_button_key):
        # Send the uploaded image to the image prediction backend
        image_data = image_upload.read()
        files = {"image": ("image.jpg", image_data, "image/jpeg")}
        image_prediction_response = requests.post("http://localhost:5001/predict", files=files)
        if image_prediction_response.status_code == 200:
            predicted_name = json.loads(image_prediction_response.text)["predicted_name"]
            st.markdown(f"**Predicted Name: {predicted_name}**", unsafe_allow_html=True)
            # Store the uploaded image and predicted name in the session state
            st.session_state.uploaded_image = image_data
            st.session_state.predicted_name = predicted_name

# Display the uploaded image
if st.session_state.uploaded_image is not None:
    st.image(Image.open(io.BytesIO(st.session_state.uploaded_image)))