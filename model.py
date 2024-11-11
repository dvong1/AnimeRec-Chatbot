import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

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
    
    # Check if the user mentions specific criteria like genre, score, or popularity
    genres = [genre for genre in df['Genres'].unique() if genre.lower() in user_input_lower]
    score_criteria = None
    popularity_criteria = None

    # Parse numerical ranges for scores and popularity
    if "score above" in user_input_lower or "rating above" in user_input_lower:
        score_criteria = float(user_input.split("score above")[-1].strip())
    elif "popular" in user_input_lower:
        popularity_criteria = "popular"

    # Filter based on the criteria
    filtered_df = df
    if genres:
        genre_regex = "|".join(genres)
        filtered_df = filtered_df[filtered_df['Genres'].str.contains(genre_regex, case=False)]
    if score_criteria:
        filtered_df = filtered_df[filtered_df['Score'] >= score_criteria]
    if popularity_criteria == "popular":
        filtered_df = filtered_df.sort_values(by='Popularity').head(5)  # Assuming lower Popularity ranks are better

    # Sort by score for general recommendations and limit to top 5
    filtered_df = filtered_df.sort_values(by='Score', ascending=False).head(5)

    # Return recommendations with more detailed descriptions
    if not filtered_df.empty:
        recommendations = []
        for _, row in filtered_df.iterrows():
            recommendations.append(
                f"**{row['Name']}**\n"
                f"**Type**: {row['Type']} | **Episodes**: {row['Episodes']} | **Source**: {row['Source']}\n"
                f"**Genres**: {row['Genres']}\n"
                f"**Score**: {row['Score']}\n"
                f"**Synopsis**: {row['Synopsis'][:250]}..."  # Limiting synopsis length for clarity
            )
        return "Here are the top anime recommendations based on your preferences:\n\n" + "\n\n".join(recommendations)
    else:
        return "I'm sorry, I couldn't find any anime that matches your criteria."

# Example function to generate a response with the model
def generate_response(user_input):
    # Generate an AI response using the model for conversational polish
    input_ids = tokenizer.encode(user_input, return_tensors='pt')
    bot_output = model.generate(input_ids, max_length=150, num_return_sequences=1, temperature=0.7)
    response_text = tokenizer.decode(bot_output[0], skip_special_tokens=True)

    # Combine recommendation logic with language model's output
    recommendation = recommend_anime(user_input)
    return f"{response_text}\n\n{recommendation}"
