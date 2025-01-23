# Music Playlist & Song Analysis App

## Overview
This Python application allows users to create custom music playlists based on song titles, artists, or genres using OpenAI's GPT-4 model and Spotify API. Additionally, it provides powerful song analysis capabilities, such as sentiment analysis, word frequency analysis, n-grams, named entity recognition, syntactic analysis, and more.

The app also features a text-to-speech functionality using ElevenLabs to read out the analysis of the song lyrics.

## Features
- **Create Playlists**: Generate personalized playlists based on song titles, genres, or artists using OpenAI's GPT-4 model.
- **Song Analysis**: Analyze song lyrics using various methods:
  - **Sentiment Analysis**: Determine the emotional tone of the lyrics.
  - **Word Frequency**: Identify the most frequently used words in the lyrics.
  - **N-Gram Analysis**: Find common phrases or word combinations in the lyrics.
  - **Named Entity Recognition (NER)**: Detect named entities such as places, people, and more in the lyrics.
  - **Syntactic Analysis**: Analyze sentence structures and parts of speech in the lyrics.
- **Text-to-Speech**: Convert song analysis text to speech and play it back using ElevenLabs.
- **Current Playlists**: View and access your existing Spotify playlists.

## Technologies Used
- **Python**: The core language used for this project.
- **OpenAI GPT-4**: For generating song recommendations and analyzing song lyrics.
- **Spotipy**: For interacting with the Spotify API to create playlists and search for songs.
- **ElevenLabs**: For converting the song analysis into audio.
- **Tkinter**: For creating a graphical user interface (GUI).
- **NLTK**: For sentiment analysis using VADER.
- **spaCy**: For named entity recognition and syntactic analysis.
- **TextBlob**: For additional sentiment analysis (polarity and subjectivity).
- **Matplotlib**: For visualizing word frequency and n-gram analysis.

## Installation

### Prerequisites
Make sure you have Python 3.7+ installed. You will also need the following instructions:

#### Step 1: Activate your virtual environment
If you're using a virtual environment (which is a good idea), activate it:

**On Windows:**
```bash
.\venv\Scripts\activate
```
##### Step 2: Generate the requirements.txt file
After activating the environment, run the command:

pip freeze > requirements.txt

## Setup ##
Setup
1. Clone the repository to your local machine:

```bash 
git clone https://github.com/Mateusz-Grencel/analiza_piosenek
```

2. Insert the API keys for OpenAI, Spotify, and ElevenLabs into the api_keys.py file.

2. Run the application:
```
python main.py
```

## Usage

### Main Features:
- **Create Playlist**: Enter a song title, artist, or genre to generate a playlist.
- **Analyze Song**: Enter a song title to analyze its lyrics using different analysis methods (e.g., sentiment, word frequency, n-grams).
- **Current Playlists**: View and access your existing Spotify playlists.
- **Text-to-Speech**: Listen to the analysis of song lyrics read aloud.

### UI Walkthrough:
Upon running the app, you will see the main interface where you can:
- Create a playlist by entering song details.
- Analyze a song by selecting an analysis method and entering a song title.
- View your current playlists.

## Contributions
Contributions are welcome! Please fork the repository, make changes, and submit pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
- **OpenAI**: For providing powerful AI models to analyze and generate music recommendations.
- **Spotify**: For providing access to a vast music library via their API.
- **ElevenLabs**: For enabling text-to-speech capabilities.
- **spaCy**: For advanced NLP tasks like named entity recognition and syntactic analysis.
- **NLTK**: For sentiment analysis using VADER.
- **Matplotlib**: For visualizing analysis results.
