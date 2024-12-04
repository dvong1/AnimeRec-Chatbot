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

# Define possible genres as a dictionary
GENRES = {
    "sports": "Sports",
    "comedy": "Comedy",
    "action": "Action",
    "fantasy": "Fantasy",
    "drama": "Drama",
    "adventure": "Adventure",
    "romance": "Romance",
    "sci-fi": "Sci-Fi",
    "supernatural": "Supernatural",
    "mystery": "Mystery",
    "horror": "Horror",
    "slice of life": "Slice of Life",
    "award winning": "Award Winning",
    "suspense": "Suspense"
}

def parse_user_input(user_input):
    """
    Parse user input to identify genres and other criteria.
    Returns a dictionary with identified genres and other filters.
    """
    user_input_lower = user_input.lower().split()
    genres = set()
    filters = {}

    # Check for genres
    for word in user_input_lower:
        if word in GENRES:
            genres.add(GENRES[word])
    
    # Add more parsing logic for other filters if needed (e.g., Type, Episodes)
    # Example: Check for "movie" or "TV"
    if "movie" in user_input_lower:
        filters["Type"] = "Movie"
    elif "tv" in user_input_lower:
        filters["Type"] = "TV"
    
    # Return identified genres and filters
    return {
        "genres": genres,
        "filters": filters
    }

def recommend_anime(user_input):
    parsed_input = parse_user_input(user_input)
    genres = parsed_input["genres"]
    filters = parsed_input["filters"]
    num_recommendations = 5

    # Filter by genres
    if genres:
        genre_filter = df['Genres'].str.contains('|'.join(genres), case=False, na=False)
        filtered_df = df[genre_filter]
    else:
        # If no genre is specified, use the entire dataset
        filtered_df = df

    # Apply additional filters (e.g., Type)
    for key, value in filters.items():
        filtered_df = filtered_df[filtered_df[key] == value]

    # Sort by score
    filtered_df = filtered_df.sort_values(by=['Score'], ascending=False)
    
    # Limit to top 50
    top_anime = filtered_df.head(50)

    # Apply controlled randomization
    if len(top_anime) > num_recommendations:
        recommended_anime = top_anime.sample(n=num_recommendations, random_state=random.randint(0, 1000))
    else:
        recommended_anime = top_anime
    
    # Format recommendations
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