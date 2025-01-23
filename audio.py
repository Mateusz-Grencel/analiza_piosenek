from elevenlabs import ElevenLabs
import os
import openai
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from api_keys import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET,ELEVENLABS_API_KEY

# Inicjalizacja klienta ElevenLabs
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# Ustawienia autoryzacji OAuth dla Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri="https://127.0.0.1",
                                               scope=["playlist-modify-public", "playlist-modify-private"]))

# Funkcja do generowania analizy tekstowej piosenki na podstawie tytułu i artysty
def generate_song_analysis(song_title_input):
    # Wyszukiwanie piosenki na Spotify, aby uzyskać autora
    results = sp.search(q=song_title_input, limit=1, type='track')
    if results['tracks']['items']:
        song_name = results['tracks']['items'][0]['name']
        artist_name = results['tracks']['items'][0]['artists'][0]['name']
    else:
        print(f"Nie znaleziono piosenki o tytule '{song_title_input}' na Spotify.")
        return None

    # Przygotowanie zapytania do OpenAI z uwzględnieniem autora
    prompt = f"Please provide a brief analysis of the song '{song_name}' by {artist_name}. Describe the main themes, emotions, and message of the song. Return the response in English and in 5 sentences."

    # Przygotowanie zapytania w formacie JSON do OpenAI
    data = {
        "model": "gpt-4",  # Możesz wybrać model, np. gpt-3.5-turbo
        "messages": [
            {"role": "system", "content": "You are an assistant that helps analyze song lyrics."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150
    }

    # Wywołanie API OpenAI
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        data=json.dumps(data)
    )

    # Sprawdzamy, czy odpowiedź jest poprawna
    if response.status_code == 200:
        result = response.json()
        analysis = result['choices'][0]['message']['content'].strip()
        print(f"Analysis for song '{song_name}' by {artist_name}: {analysis}")  # Debugging output
        return analysis
    else:
        print(f"Error with OpenAI API: {response.status_code}")
        return None


# Funkcja do konwertowania tekstu na mowę i odtwarzania go
def play_audio(song_title):
    # Sprawdzenie, czy folder 'output_audio' istnieje, jeśli nie, tworzymy go
    if not os.path.exists('./output_audio'):
        os.makedirs('./output_audio')

    # Uzyskanie analizy tekstu piosenki
    analysis = generate_song_analysis(song_title)

    if analysis:
        # Jeśli analiza jest dostępna, konwertujemy ją na mowę
        audio_generator = client.text_to_speech.convert(
            voice_id="ZUdFQHf8lAj4o7hiHvbE",  # Zmień na odpowiedni voice_id
            output_format="mp3_44100_128",
            text=analysis
        )

        # Zapis audio do pliku
        audio_file_path = f"./output_audio/{song_title}_audio.mp3"
        with open(audio_file_path, "wb") as f:
            # Odczytujemy dane z generatora i zapisujemy do pliku
            for chunk in audio_generator:
                f.write(chunk)
    else:
        print("Brak dostępnej analizy do konwersji na mowę.")
