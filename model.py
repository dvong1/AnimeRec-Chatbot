import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the model and tokenizer
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Load your anime dataset
df = pd.read_csv('filtered_anime.csv')

# Strip whitespace from the relevant columns to ensure clean comparisons
df['Name'] = df['Name'].str.strip()
df['English name'] = df['English name'].str.strip()
df['Genres'] = df['Genres'].str.strip()
df['Synopsis'] = df['Synopsis'].str.strip()

# Function to recommend anime based on user input
def recommend_anime(user_input):
    user_input_lower = user_input.lower()
    
    # List of anime titles to check against
    anime_titles = df['Name'].str.lower().tolist() + df['English name'].str.lower().tolist()

    # Extract anime title from the input
    matched_titles = [title for title in anime_titles if title in user_input_lower]

    if matched_titles:
        # Get the first matched title for simplicity
        matched_title = matched_titles[0]
        
        # Find the corresponding anime entry in the DataFrame
        anime_entry = df[(df['Name'].str.lower() == matched_title) | 
                         (df['English name'].str.lower() == matched_title)].iloc[0]
        
        return (f"I recommend **{anime_entry['Name']}** because it is a/an **{anime_entry['Genres']}** "
                f"anime with a score of **{anime_entry['Score']}**. Here's a brief synopsis: {anime_entry['Synopsis']}")
    else:
        return "I'm sorry, I couldn't find any recommendations based on your input."


# Example function to generate a response from the model
def generate_response(user_input):
    return recommend_anime(user_input)
