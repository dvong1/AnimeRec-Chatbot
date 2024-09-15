# AnimeRec-Chatbot
This is a class project where a chatbot will recommend anime based on user preference. It will use an already trained A.I. model as its core.

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