import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
import random

# Load the model and tokenizer
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Load your anime dataset
df = pd.read_csv('filtered_anime.csv')

# Strip whitespace from relevant columns to ensure clean comparisons
df['Name'] = df['Name'].str.strip()
df['English name'] = df['English name'].str.strip()
df['Genres'] = df['Genres'].str.strip()
df['Synopsis'] = df['Synopsis'].str.strip()

# Enhanced recommendation function
def recommend_anime(user_input):
    user_input_lower = user_input.lower()
    num_recommendations = 5
    
    # Step 1: Extract Keywords (Basic NLP)
    input_keywords = set(user_input_lower.split())
    
    # Step 2: Match Genre from Dataset
    matched_genres = df['Genres'].str.lower().apply(
        lambda x: int(any(word in x for word in input_keywords))
    )
    genre_filtered_df = df[matched_genres > 0]
    
    # Step 3: Sort by Score
    genre_filtered_df = genre_filtered_df.sort_values(by=['Score'], ascending=False)
    
    # Step 4: Limit to Top 100
    top_genre_anime = genre_filtered_df.head(100)
    
    # Step 5: Apply Controlled Randomization
    if len(top_genre_anime) > num_recommendations:
        recommended_anime = top_genre_anime.sample(n=num_recommendations, random_state=random.randint(0, 1000))
    else:
        recommended_anime = top_genre_anime
    
    # Step 6: Format Recommendations
    recommendations = []
    for _, row in recommended_anime.iterrows():
        recommendations.append(
            f"**{row['Name']}**\n"
            f"**Type**: {row['Type']} | **Episodes**: {row['Episodes']} | **Source**: {row['Source']}\n"
            f"**Genres**: {row['Genres']}\n"
            f"**Score**: {row['Score']}\n"
            f"**Synopsis**: {row['Synopsis'][:250]}..."
        )
    
    return "Here are the top anime recommendations based on your preferences:\n\n" + "\n\n".join(recommendations)

# Example function to generate a response with the model
def generate_response(user_input):
    # Generate an AI response using the model for conversational polish

    # Combine recommendation logic with language model's output
    recommendation = recommend_anime(user_input)
    return recommendation