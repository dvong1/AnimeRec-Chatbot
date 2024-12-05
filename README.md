# **Anime Recommendation Chatbot**
  By: David Vong, Justin Nguyen, Danny Tran

## **Project Overview**
The Anime Recommendation System is a web application that provides personalized anime recommendations based on user input. Built using **Streamlit** for an intuitive and interactive user interface, the project employs a lightweight recommendation logic that filters anime by genre, score, and other attributes to generate tailored suggestions.  

This system leverages a dataset of anime metadata, including genres, episode counts, and synopsis, to match user preferences and deliver high-quality recommendations.


## **Features**
- **Keyword-Based Input:** Accepts natural language input and extracts relevant keywords (e.g., genres or themes).
- **Personalized Recommendations:** Filters top-rated anime by matching genres and controlled randomization.
- **Interactive Web UI:** Easy-to-use interface powered by Streamlit for seamless user interaction.
- **Data-Driven Suggestions:** Ranks anime by their scores, ensuring only top-rated shows are recommended.


## **Installation and Setup**

Follow the steps below to set up the project on your local machine:

### **1. Clone the Repository**
  ```
  git clone https://github.com/dvong1/AnimeRec-Chatbot.git
  ```

### **2. Set Up a Virtual Environment**
It’s best to use a virtual environment to isolate dependencies and avoid conflicts:
- For **Windows**:
  ```
  python -m venv venv
  venv\Scripts\activate
  ```
- For **MacOS/Linux**:
  ```
  python3 -m venv venv
  source venv/bin/activate
  ```

### **3. Install Required Packages**
After activating your virtual environment, install the dependencies using `requirements.txt`:
  ```
  pip install -r requirements.txt
  ```

### **4. Run the Application**
Start the Streamlit app by running the following command:
  ```
  streamlit run app.py
  ```

## **How to Use**
1. Enter Preferences: Type in your anime preferences (e.g., “I like sports anime” or “Give me action anime”).
2. Receive Recommendations: The app will display a list of top 5 recommendations tailored to your input.
3. Explore Results: Each recommendation includes the anime's type, episode count, genres, score, and a brief synopsis.

## **License**
This project is for educational purposes only and is not intended for commercial use. The anime dataset used in this project may be subject to copyright.

## **Acknowledgements**
Special thanks to our professor, MyAnimeList, Kaggle and Streamlit!

## Requirements
- Python3.9


## Getting Started

Open your intepreter and clone the git repo.<br>

Within the opened project, open a terminal window.<br>

Switch to the development branch. You can run this command to checkout
```bash
git checkout 
```

Make sure the repo is up to date with the following command
```bash
git pull origin development
```

Download the required packages with the command
```bash
pip install -r requirements.txt
```

Start developing! I will outline goals and future features for our development branch here.
- Create vector database for the anime csv (We can use Vector package or create our own SQL vector DB)
- Design system to retrieve data from vector DB
- Implement generative A.I. with chosen GPT
- Create text-generation component based on user prompt