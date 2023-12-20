import streamlit as st
import torch
from transformers import pipeline
from gpt import create_prompt

st.title("Culinary Curator - Recipe Recommendation System")

# Create an input field for user input of ingredients
ingredients = st.text_area("Enter Ingredients (comma-separated):")

# Create a button to trigger recipe generation
if st.button("Generate Recipe"):
    # Call your recipe generation function
    x = create_prompt(ingredients)
    # Display the generated recipe
    st.write("Generated Recipe:")
    st.write(x)
