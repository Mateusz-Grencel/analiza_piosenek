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
Make sure you have Python 3.7+ installed. You will also need the following dependencies:
