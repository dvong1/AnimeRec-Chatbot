import sys

from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_chat import message
from langchain_community.document_loaders import CSVLoader  # Updated import
from langchain.vectorstores import FAISS  # Using FAISS for vector storage
from langchain.embeddings.openai import OpenAIEmbeddings  # OpenAI embeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI  # Updated import
from model import generate_response # import generative text function 

# Page config
st.set_page_config(
    page_title="Anime-Chatbot",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "# Find your next Anime!!"}
)

# Function to handle navigation
def navigation_menu():
    selected_page = st.sidebar.selectbox(
        "Choose a page", ["Anime ChatBot", "Anime Data Visualization"])
    return selected_page

# Anime DataFrame
df = pd.read_csv('filtered_anime.csv')
df = df[["Name", "Rank", "Score", "Genres", "Type", "Episodes", "Source", "Popularity", 'Aired']]

# Navigation

# Sidebar options for navigation across pages
st.sidebar.title("Navigation")
st.sidebar.markdown("Use the options below to navigate through the dashboard.")
selected_page = navigation_menu()

# Page 1: ChatBot functionality
if selected_page == "Anime ChatBot":
    # Main Title and Subtitles
    st.markdown("<h1 style='text-align: center; font-weight:bold; font-family:cursive; color:red;'>Anime ChatBot</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color:gray; font-style:italic;'>Discover Your Next Anime Adventure!</h2>", unsafe_allow_html=True)

    # Display the Anime Dataset with enhanced styling
    st.markdown("### Anime Dataset Overview")
    st.markdown("Explore popular anime titles along with their genres, ratings, and more. Use this table to find your favorite genres or highly-rated shows.")
    st.dataframe(df.style.set_properties(**{
    'background-color': '#FFFFFF',  # Set background color to white
    'color': '#000000',  # Set text color to black
    'border-color': '#4A90E2',
    'font-size': '14px',
    'font-family': 'Arial'
}), height=500, hide_index=True)

    # Sidebar for Chatbot Interaction and Navigation
    st.sidebar.title("Explore Anime Trends")
    st.sidebar.markdown("**Visualize anime data or interact with our chatbot to get recommendations!**")

    # Load dataset into session state if not already present
    if "datasets" not in st.session_state:
        datasets = {}
        datasets["Anime Data"] = df
        st.session_state["datasets"] = datasets

    with st.sidebar:
        dataset_container = st.empty()
 
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Accept user input for chatbot
    prompt = st.chat_input("Ask me for anime recommendations or tell me what genres you like!")

    # Process user input and chatbot response
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get recommendation from the model
        response = generate_response(prompt)

        # Add bot's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Display chat history
    st.markdown("<div style='margin-top: 20px; border-top: 1px solid #ddd; padding-top: 10px;'>", unsafe_allow_html=True)
    for message in st.session_state.messages:
        role_style = "color:#4A90E2;" if message["role"] == "assistant" else "color:#333;"
        with st.chat_message(message["role"]):
            st.markdown(f"<span style='{role_style}'>{message['content']}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Page 2: Visualization functionality
elif selected_page == "Anime Data Visualization":
    st.title("Anime Data Visualization")
    st.subheader("Explore the Distribution of Anime Genres, Scores, and Episodes")

    # Genre Distribution Pie Chart
    st.markdown("### Anime Genre Distribution")
    st.markdown("This pie chart represents the distribution of anime genres within the dataset, giving insight into the popularity of each genre based on the number of titles.")
    
    # Extract genres from the 'Genres' column, split by commas, and clean up spaces
    all_genres = []
    for genres in df['Genres'].dropna():
        all_genres.extend([genre.strip() for genre in genres.split(',')])

    # Create a DataFrame with genre counts
    genre_df = pd.DataFrame(all_genres, columns=['Genres']).value_counts().reset_index()
    genre_df.columns = ['Genres', 'Count']

    # Create a pie chart
    fig_genre = px.pie(
        genre_df,
        values='Count',
        names='Genres',
        title='Anime Genres Distribution',
        color_discrete_sequence=px.colors.qualitative.Set3  # Professional color scheme
    )
    st.plotly_chart(fig_genre)
    
    # Score Distribution Histogram
    st.markdown("### Distribution of Anime Scores")
    st.markdown("This histogram illustrates the distribution of anime scores across the dataset, with the x-axis representing the score range and the y-axis representing the number of anime titles. It provides an overview of the rating tendencies within the dataset.")

    # Handle scores and create histogram
    scores = pd.to_numeric(df['Score'], errors='coerce').dropna()
    fig_scores = px.histogram(
        scores,
        nbins=20,
        title='Distribution of Anime Scores',
        labels={'value': 'Score', 'count': 'Number of Animes'},
        color_discrete_sequence=['#1f77b4']  # Color for the histogram bars
    )
    fig_scores.update_layout(
        xaxis_title="Score",
        yaxis_title="Number of Animes",
        bargap=0.1
    )
    st.plotly_chart(fig_scores)

    # Episode Range Bar Chart
    st.markdown("### Distribution by Number of Episodes")
    st.markdown("This bar chart shows anime titles filtered by the selected episode range, allowing for exploration of titles with varying episode lengths.")
        
    # Ensure 'Episodes' column is numeric, coerce errors to handle non-numeric values
    df['Episodes'] = pd.to_numeric(df['Episodes'], errors='coerce')

    # Drop rows where 'Episodes' is NaN (non-numeric values are converted to NaN in the above step)
    df = df.dropna(subset=['Episodes'])

    # Convert 'Episodes' to integer if needed
    df['Episodes'] = df['Episodes'].astype(int)
    
    # Sidebar dropdown for episode range selection
    episode_ranges = {
        "1-12 episodes": (1, 12),
        "13-24 episodes": (13, 24),
        "25-50 episodes": (25, 50),
        "51+ episodes": (51, float('inf'))
    }
    selected_range = st.sidebar.selectbox("Select Episode Range", list(episode_ranges.keys()))

    # Filter dataset based on selected episode range
    min_episodes, max_episodes = episode_ranges[selected_range]
    df_filtered = df[(df['Episodes'] >= min_episodes) & (df['Episodes'] <= max_episodes)]

    # Create a bar chart of anime titles by episode count within the selected range
    fig_episodes = px.bar(
        df_filtered,
        x='Name',
        y='Episodes',
        title=f"Anime Titles with {selected_range}",
        labels={'Name': 'Anime Title', 'Episodes': 'Number of Episodes'},
        color_discrete_sequence=['#ff7f0e']  # Color for the bar chart
    )
    fig_episodes.update_layout(
        xaxis={'categoryorder': 'total descending'},
        xaxis_title="Anime Title",
        yaxis_title="Number of Episodes"
    )
    st.plotly_chart(fig_episodes)


    # Add new section for Timeframe Distribution
    st.markdown("### Distribution of Anime by Release Year")
    st.markdown("This bar chart shows how many anime titles were released within the selected time frame.")

    # Ensure 'Aired' column is parsed correctly to extract the year
    df['Year'] = pd.to_datetime(df['Aired'], errors='coerce').dt.year
    df = df.dropna(subset=['Year'])  # Remove any rows where the year could not be parsed

    # Create initial plot (all anime titles)
    fig_years = px.histogram(
        df,
        x='Year',
        title="Number of Anime Titles Released Per Year",
        labels={'Year': 'Release Year', 'count': 'Number of Titles'},
        color_discrete_sequence=['#007bff ']  # Color for the histogram
    )
    fig_years.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Anime Titles",
        bargap=0.1
    )
    st.plotly_chart(fig_years)

# Timeframe selection for user
    year_range = st.slider(
        "Select Year Range",
        min_value=int(df['Year'].min()),  
        max_value=int(df['Year'].max()), 
        value=(int(df['Year'].min()), int(df['Year'].max())), 
        step=1 
    )


    # Filter dataset based on selected year range
    df_filtered_years = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

    # Plot the filtered data based on the selected range
    fig_filtered_years = px.histogram(
        df_filtered_years,
        x='Year',
        title=f"Number of Anime Titles Released Between {year_range[0]} and {year_range[1]}",
        labels={'Year': 'Release Year', 'count': 'Number of Titles'},
        color_discrete_sequence=['#007bff ']  # Color for the histogram
    )
    fig_filtered_years.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Anime Titles",
        bargap=0.1
    )
    st.plotly_chart(fig_filtered_years)



