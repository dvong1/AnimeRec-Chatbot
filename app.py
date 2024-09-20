import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Anime-Chatbot",
    layout="wide",
    menu_items={
        'About': "# Find your next Anime!!"
    }              
                   )

st.title("Anime Chatbot")

df = pd.read_csv('anime-dataset-2023.csv')

st.dataframe(df, height=500, hide_index=True)