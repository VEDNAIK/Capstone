import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the SentenceTransformer model
bert = SentenceTransformer('bert-base-nli-mean-tokens')

# Load the DataFrame from CSV
df = pd.read_csv('string_ingredients.csv')

# Load precomputed sentence embeddings
sentence_embeddings = np.load('sentence_embeddings.npy')

def custom(input_str):
    try:
        # Encode the input string using BERT
        input_embedding = bert.encode(input_str)

        # Compute cosine similarities between the input and all recipes
        similarities = cosine_similarity(sentence_embeddings, input_embedding.reshape(1, -1))

        # Get the indices of the top 10 most similar recipes
        top_indices = similarities.argsort(axis=0)[-10:][::-1].flatten()

        # Create a DataFrame with the recommended recipes
        recommendation_data = df.iloc[top_indices]
        recommendation_data = recommendation_data.reset_index(drop=True)
        return recommendation_data
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example input
input_str = "salt, potato, oil"
result = custom(input_str)
print(result)