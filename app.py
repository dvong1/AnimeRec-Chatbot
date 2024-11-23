import pandas as pd
import streamlit as st
import altair as alt
from streamlit_chat import message
from langchain_community.document_loaders import CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from model import generate_response  # Import generative text function

# Page configuration
st.set_page_config(
    page_title="Anime ChatBot",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "# Find your next Anime!!"}
)

# Cache data loading for performance
@st.cache_data
def load_data():
    df = pd.read_csv('filtered_anime.csv')
    df = df[["Name", "Rank", "Score", "Genres", "Type", "Episodes", "Source", "Popularity"]]
    df['Score'] = pd.to_numeric(df['Score'], errors='coerce', downcast='float')
    df['Episodes'] = pd.to_numeric(df['Episodes'], errors='coerce', downcast='integer')
    return df.dropna()

df = load_data()

# Cache genre distribution computation
@st.cache_data
def compute_genre_distribution(df):
    all_genres = []
    for genres in df['Genres'].dropna():
        all_genres.extend([genre.strip() for genre in genres.split(',')])
    genre_df = pd.DataFrame(all_genres, columns=['Genres']).value_counts().reset_index()
    genre_df.columns = ['Genres', 'Count']
    return genre_df

genre_df = compute_genre_distribution(df)

# Cache score distribution computation
@st.cache_data
def compute_score_distribution(df):
    return df['Score'].dropna()

# Cache episode distribution computation
@st.cache_data
def compute_episode_distribution(df):
    episode_ranges = {
        "1-12 episodes": (1, 12),
        "13-24 episodes": (13, 24),
        "25-50 episodes": (25, 50),
        "51+ episodes": (51, float('inf'))
    }
    return episode_ranges

episode_ranges = compute_episode_distribution(df)

# Navigation menu
def navigation_menu():
    selected_page = st.sidebar.selectbox("Choose a page", ["Anime ChatBot", "Anime Data Visualization"])
    return selected_page

selected_page = navigation_menu()

# ChatBot functionality
if selected_page == "Anime ChatBot":
    # Title and Subtitles
    st.markdown("<h1 style='text-align: center; font-weight:bold; font-family:cursive; color:red;'>Anime ChatBot</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color:gray; font-style:italic;'>Discover Your Next Anime Adventure!</h2>", unsafe_allow_html=True)

    # Display dataset
    st.markdown("### Anime Dataset Overview")
    st.dataframe(df, height=500)

    # Chat history initialization
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # User input for chatbot
    prompt = st.chat_input("Ask me for anime recommendations or tell me what genres you like!")

    # Process input and generate response
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = generate_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Display chat history with a limit
    MAX_HISTORY_LENGTH = 20
    st.session_state.messages = st.session_state.messages[-MAX_HISTORY_LENGTH:]
    for message in st.session_state.messages:
        role_style = "color:#4A90E2;" if message["role"] == "assistant" else "color:#333;"
        with st.chat_message(message["role"]):
            st.markdown(f"<span style='{role_style}'>{message['content']}</span>", unsafe_allow_html=True)

# Visualization functionality
elif selected_page == "Anime Data Visualization":
    st.title("Anime Data Visualization")
    st.subheader("Explore the Distribution of Anime Genres, Scores, and Episodes")

    # Genre Distribution Pie Chart
    st.markdown("### Anime Genre Distribution")
    genre_chart = alt.Chart(genre_df).mark_bar().encode(
        x=alt.X('Genres', sort='-y'),
        y='Count',
        color=alt.Color('Genres', legend=None)
    ).properties(title="Anime Genre Distribution").interactive()
    st.altair_chart(genre_chart, use_container_width=True)

    # Score Distribution Histogram
    st.markdown("### Distribution of Anime Scores")
    scores = compute_score_distribution(df)
    score_chart = alt.Chart(pd.DataFrame(scores, columns=['Score'])).mark_bar().encode(
        alt.X('Score:Q', bin=alt.Bin(maxbins=20)),
        y='count()'
    ).properties(title="Distribution of Anime Scores")
    st.altair_chart(score_chart, use_container_width=True)

    # Episode Range Bar Chart
    st.markdown("### Distribution by Number of Episodes")
    selected_range = st.sidebar.selectbox("Select Episode Range", list(episode_ranges.keys()))
    
    min_episodes, max_episodes = episode_ranges[selected_range]
    df_filtered = df[(df['Episodes'] >= min_episodes) & (df['Episodes'] <= max_episodes)]
    
    episode_chart = alt.Chart(df_filtered).mark_bar().encode(
        x=alt.X('Name:N', sort='-y'),
        y='Episodes:Q',
        color=alt.ColorValue("#ff7f0e")
    ).properties(title=f"Anime Titles with {selected_range}").interactive()
    
    st.altair_chart(episode_chart, use_container_width=True)

    # Additional Visualizations

    # Popularity vs Score Scatter Plot
    st.markdown("### Popularity vs Score")
    popularity_score_chart = alt.Chart(df).mark_circle(size=60).encode(
        x='Popularity',
        y='Score',
        color='Genres',
    ).properties(title="Popularity vs Score").interactive()
    st.altair_chart(popularity_score_chart, use_container_width=True)

    # Type Distribution Pie Chart
    st.markdown("### Anime Type Distribution")
    type_df = df['Type'].value_counts().reset_index()
    type_df.columns = ['Type', 'Count']
    type_chart = alt.Chart(type_df).mark_arc().encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="Type", type="nominal"),
        tooltip=['Type', 'Count']
    ).properties(title="Anime Type Distribution").interactive()
    st.altair_chart(type_chart, use_container_width=True)
    
