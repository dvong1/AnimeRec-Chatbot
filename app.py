import sys
import os
from pathlib import Path
import streamlit as st
import pandas as pd
import openai
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
df = df[["Name", "Rank","Score", "Genres","Type", "Episodes", "Source", "Popularity"]]

# Navigation
selected_page = navigation_menu()

# # Page 1: ChatBot functionality
# default_text = st.text_area("Input some text here", "default text")
# st.write(default_text)

if selected_page == "Anime ChatBot":
    # Main Title and Subtitles
    st.markdown("<h1 style='text-align: center; font-weight:bold; font-family:comic sans ms; padding-top: 0rem;'> Anime ChatBot </h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;padding-top: 0rem;'>Discover Your Next Anime Adventure!</h2>", unsafe_allow_html=True)

    # Display the dataset
    st.dataframe(df, height=500, hide_index=True)

    # Sidebar for Chatbot interaction
    st.sidebar.title("Explore Anime Trends")
    st.sidebar.markdown("**Visualize anime data:**")

    if "datasets" not in st.session_state:
        datasets = {}
        datasets["Anime Data"] = pd.read_csv("filtered_anime.csv")
        st.session_state["datasets"] = datasets

    with st.sidebar:
        dataset_container = st.empty()
 
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Accept user input
    prompt = st.chat_input("Ask me for anime recommendations!")

    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get recommendation from the model
        response = generate_response(prompt)

        # Add bot's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display both the user input and bot response
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


# Page 2: Visualization functionality
elif selected_page == "Anime Data Visualization":
    st.title("Anime Data Visualization")
    st.subheader("Explore the Distribution of Anime Genres and Scores")

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

# Sidebar options for navigation across pages
st.sidebar.title("Navigation")
st.sidebar.markdown("Use the options below to navigate through the dashboard.")

