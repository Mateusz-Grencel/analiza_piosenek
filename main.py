import tkinter as tk
from tkinter import ttk
import openai
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pyperclip
from song_lyrics import get_song_lyrics
from text_analysis import analyze_song_and_save
from audio import play_audio

# Ustawienie klucza API OpenAI
openai.api_key = "OpenAI_KEY"

# Ustawienia autoryzacji OAuth dla Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="client_id",
                                               client_secret="client_secret",
                                               redirect_uri="https://127.0.0.1",
                                               scope=["playlist-modify-public", "playlist-modify-private"]))

def create_playlist(root, label, stworzenie_playlisty, aktualne_playlisty, analiza_piosenki, main_image_l):
    # Ukrywamy główny ekran
    label.pack_forget()
    stworzenie_playlisty.pack_forget()
    aktualne_playlisty.pack_forget()
    analiza_piosenki.pack_forget()
    main_image_l.pack_forget()

    root.title("Tworzenie playlisty")

    # Etykieta powitalna
    create_playlist_image = tk.PhotoImage(file="Stworzenie_playlisty.png")
    # Tworzymy Label z obrazkiem
    create_playlist_l = tk.Label(root, image=create_playlist_image)
    # Zapisujemy referencję do obrazka
    create_playlist_l.image = create_playlist_image  # Zapisujemy referencję do obrazka
    # Wyświetlamy obrazek
    create_playlist_l.pack()

    # Tworzenie etykiety dla nazwy playlisty
    playlist_name_label = tk.Label(root, text="Wpisz nazwę playlisty", font=("Arial", 14))
    playlist_name_label.pack(pady=10, padx=10)

    # Tworzenie pola tekstowego dla nazwy playlisty
    playlist_name_entry = tk.Entry(root, font=("Arial", 14))
    playlist_name_entry.pack(pady=10, padx=10)

    # Tworzenie etykiety
    things = tk.Label(root, text="Wpisz tytuł piosenki, nazwę autora bądź gatunek", font=("Arial", 14))
    things.pack(pady=10, padx=10)

    # Tworzenie pola tekstowego
    text_entry = tk.Entry(root, font=("Arial", 14))
    text_entry.pack(pady=10, padx=10)

    # Tworzenie przycisku do tworzenia playlisty
    button = tk.Button(root, text="Stwórz playlistę", font=("Arial", 14), command=lambda: generate_playlist(playlist_name_entry, text_entry, root))
    button.pack(pady=20, padx=10)

    # Przycisk powrotu do ekranu głównego
    powrot_na_glowna = tk.Button(root, text="Powrót na stronę główną", font=("Arial", 14),
                                 command=lambda: back_to_main_screen(root, label, stworzenie_playlisty, aktualne_playlisty, analiza_piosenki))
    powrot_na_glowna.pack(pady=20, padx=10)

def generate_playlist(playlist_name_entry, text_entry, root):
    playlist_name = playlist_name_entry.get()  # Pobranie nazwy playlisty
    input_text = text_entry.get()  # Pobranie tekstu z pola tekstowego

    prompt = f"Podaj dokładnie 10 piosenek na podstawie: {input_text} i nic więcej"

    # Przygotowanie zapytania w formacie JSON do OpenAI
    data = {
        "model": "gpt-4",  # Możesz wybrać model, np. gpt-3.5-turbo
        "messages": [
            {"role": "developer", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 100
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
        songs = result['choices'][0]['message']['content'].strip()

        print("OpenAI response:", songs)  # Debugging response

        # Tworzenie playlisty na Spotify
        song_list = songs.split('\n')
        song_uris = []

        for song in song_list:
            song_info = song.split('"')
            if len(song_info) > 1:
                song_name = song_info[1].strip()  # Pobieramy nazwę piosenki
                search_results = sp.search(q=song_name, limit=1, type='track')
                print(f"Searching for: {song_name}")  # Debugging song search
                if search_results['tracks']['items']:
                    song_uri = search_results['tracks']['items'][0]['uri']
                    song_uris.append(song_uri)
                else:
                    print(f"Song not found: {song_name}")

        if song_uris:
            user_id = sp.current_user()['id']
            playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description="Opis playlisty")
            sp.playlist_add_items(playlist['id'], song_uris)

            # Wyświetlanie linku do playlisty
            playlist_link = f"https://open.spotify.com/playlist/{playlist['id']}"

            # Tworzymy etykiety z nazwą playlisty i linkiem pod przyciskiem "Stwórz playlistę"
            playlist_label = tk.Label(root, text=f"Playlista '{playlist_name}' została utworzona!", font=("Arial", 14))
            playlist_label.pack(pady=10, padx=10)

            clickable_link = tk.Label(root, text=playlist_link, font=("Arial", 14), fg="blue", cursor="hand2")
            clickable_link.pack(pady=10, padx=10)
            clickable_link.bind("<Button-1>", lambda event: pyperclip.copy(playlist_link))  # Skopiowanie linku po kliknięciu

            # Przycisk powrotu do ekranu głównego
            powrot_na_glowna = tk.Button(root, text="Powrót na stronę główną", font=("Arial", 14),
                                         command=lambda: back_to_main_screen(root, label, stworzenie_playlisty, aktualne_playlisty, analiza_piosenki))
            powrot_na_glowna.pack(pady=20, padx=10)

        else:
            result_label = tk.Label(root, text="Nie znaleziono żadnych piosenek na Spotify.", font=("Arial", 14))
            result_label.pack(pady=10, padx=10)
    else:
        print(f"Error with OpenAI API: {response.status_code}")
        result_label = tk.Label(root, text="Wystąpił błąd podczas pobierania danych.", font=("Arial", 14))
        result_label.pack(pady=10, padx=10)

def actual_playlist(root, label, stworzenie_playlisty, aktualne_playlisty, analiza_piosenki, main_image_l):
    # Ukrywamy główny ekran
    label.pack_forget()
    stworzenie_playlisty.pack_forget()
    aktualne_playlisty.pack_forget()
    analiza_piosenki.pack_forget()
    main_image_l.pack_forget()

    # Etykieta
    actual_playlist_image = tk.PhotoImage(file="Aktualne_playlisty.png")
    # Tworzymy Label z obrazkiem
    actual_playlist_image_l = tk.Label(root, image=actual_playlist_image)
    # Zapisujemy referencję do obrazka
    actual_playlist_image_l.image = actual_playlist_image
    # Wyświetlamy obrazek
    actual_playlist_image_l.pack()

    root.title("Aktualne playlisty")

    # Wyświetlanie informacji o aktualnych playlistach
    info_label = tk.Label(root, text="Aktualne playlisty", font=("Arial", 14))
    info_label.pack(pady=10, padx=10)

    # Pobranie aktualnych playlist
    playlists = sp.current_user_playlists()['items']

    # Tworzenie etykiety dla każdej playlisty z kopiowalnym linkiem
    for playlist in playlists:
        playlist_name = playlist['name']
        playlist_url = playlist['external_urls']['spotify']

        # Wyświetlanie nazwy playlisty
        playlist_label = tk.Label(root, text=f"{playlist_name}", font=("Arial", 14))
        playlist_label.pack(pady=5, padx=10)

        # Tworzymy etykietę dla linku do playlisty
        clickable_link = tk.Label(root, text=playlist_url, font=("Arial", 12), fg="blue", cursor="hand2")
        clickable_link.pack(pady=5, padx=10)

        # Automatyczne skopiowanie linku do schowka po kliknięciu
        clickable_link.bind("<Button-1>", lambda event, url=playlist_url: pyperclip.copy(url))

    # Przycisk powrotu do ekranu głównego
    powrot_na_glowna = tk.Button(root, text="Powrót na stronę główną", font=("Arial", 14),
                                 command=lambda: back_to_main_screen(root, label, stworzenie_playlisty, aktualne_playlisty, analiza_piosenki))
    powrot_na_glowna.pack(pady=20, padx=10)
def song_analysis(root, label, stworzenie_playlisty, aktualne_playlisty, analiza_piosenki, main_image_l):
    # Ukrywamy główny ekran
    label.pack_forget()
    stworzenie_playlisty.pack_forget()
    aktualne_playlisty.pack_forget()
    analiza_piosenki.pack_forget()
    main_image_l.pack_forget()

    # Etykieta
    song_analysis_image = tk.PhotoImage(file="Analiza_piosenki.png")
    # Tworzymy Label z obrazkiem
    song_analysis_image_l = tk.Label(root, image=song_analysis_image)
    # Zapisujemy referencję do obrazka
    song_analysis_image_l.image = song_analysis_image
    # Wyświetlamy obrazek
    song_analysis_image_l.pack()

    root.title("Analiza piosenki")

    # Tworzenie etykiety dla analizy playlisty
    playlist_name = tk.Label(root, text="Wpisz nazwę playlisty:", font=("Arial", 14))
    playlist_name.pack(pady=10, padx=10)

    # Tworzenie pola tekstowego dla nazwy playlisty
    playlist_name_entry = tk.Entry(root, font=("Arial", 14))
    playlist_name_entry.pack(pady=10, padx=10)

    # Tworzenie etykiety dla tytułu piosenki
    song_label = tk.Label(root, text="Wpisz tytuł piosenki:", font=("Arial", 14))
    song_label.pack(pady=10, padx=10)

    # Tworzenie pola tekstowego dla tytułu piosenki
    song_title_entry = tk.Entry(root, font=("Arial", 14))
    song_title_entry.pack(pady=10, padx=10)

    # Tworzenie etykiety dla wyboru analiz
    analysis_label = tk.Label(root, text="Wybierz analizę:", font=("Arial", 14))
    analysis_label.pack(pady=10, padx=10)

    # Tworzenie Combobox z 7 opcjami
    song_options = [
        "Sentyment", "Częstość słów", "N-gram", "Nazwy własne",
        "Polaryzacja", "Składnia","Audio"
    ]

    # Tworzenie Combobox do wyboru jednej opcji analizy
    song_select = ttk.Combobox(root, values=song_options, font=("Arial", 14), width=20, state="readonly")
    song_select.set("Dostępne analizy")
    song_select.pack(pady=10, padx=10)

    # Etykieta do wyświetlania opisu wybranej analizy
    description_label = tk.Label(root, text="", font=("Arial", 12), wraplength=400)
    description_label.pack(pady=10, padx=10)

    # Funkcja do aktualizacji opisu analizy
    def update_description(event):
        analysis = song_select.get()
        descriptions = {
            "Sentyment": "Ocena emocjonalnego ładunku tekstu piosenki, która pozwala określić, czy dominują w nim uczucia pozytywne, negatywne czy neutralne, wykorzystując techniki NLP.",
            "Częstość słów": "Polega na zliczaniu wystąpień słów w tekście piosenki, co pomaga zidentyfikować najbardziej dominujące motywy lub tematy w utworze.",
            "N-gram": "Analiza ciągów n-słów w tekście piosenki, umożliwiająca wychwycenie częstych kombinacji słów, które mogą wskazywać na typowe zwroty lub frazy w danym gatunku muzycznym.",
            "Nazwy własne": "Identyfikowanie nazw własnych, takich jak imiona, miejsca czy marki, w tekście piosenki, co może dostarczyć informacji o kontekście, fabule czy przekazie utworu.",
            "Polaryzacja": "Badanie rozkładu emocji w piosence, pozwalające sprawdzić, jak tekst zmienia swoje nastawienie w różnych częściach, np. od negatywnego do pozytywnego.",
            "Składnia": "Analiza struktury gramatycznej zdań w piosence, która pozwala zrozumieć, jak poszczególne elementy tekstu są ze sobą powiązane, co wpływa na jego znaczenie.",
            "Audio": "Wykorzystanie danych dźwiękowych, takich jak melodia, tonacja, rytm czy tempo, w celu zrozumienia, jak wpływają one na interpretację emocjonalną tekstu piosenki."
        }
        description_label.config(text=descriptions.get(analysis, ""))

    # Bindowanie funkcji do aktualizacji opisu przy zmianie wyboru
    song_select.bind("<<ComboboxSelected>>", update_description)

    # Funkcja do analizy playlisty i piosenki
    def analyze_song():
        song_title_input = song_title_entry.get().strip()
        selected_analysis = song_select.get().strip()

        # Wywołanie funkcji get_song_lyrics z song_lyrics.py
        print(f"Analizujemy tekst piosenki: {song_title_input}")
        lyrics = get_song_lyrics(song_title_input)  # Przekazanie nazwy piosenki do funkcji
        # print(lyrics)  # Wyświetlanie tekstu piosenki w konsoli

        # Przekazanie danych do funkcji analyze_song_and_save w text_analysis.py
        analyze_song_and_save(song_title_input, lyrics, selected_analysis)

        if selected_analysis == "Audio":
            play_audio(song_title_input)  # Generowanie pliku audio

    # Tworzenie przycisku do analizy piosenki
    song_anal = tk.Button(root, text="Analizuj piosenkę", font=("Arial", 14), command=analyze_song)
    song_anal.pack(pady=10, padx=10)

    # Przycisk powrotu do ekranu głównego
    powrot_na_glowna = tk.Button(root, text="Powrót na stronę główną", font=("Arial", 14),
                                 command=lambda: back_to_main_screen(root, label, stworzenie_playlisty,
                                                                     aktualne_playlisty, analiza_piosenki))
    powrot_na_glowna.pack(pady=20, padx=10)

def back_to_main_screen(root, label, stworzenie_playlisty, aktualne_playlisty, analiza_piosenki):
    # Ukrywamy ekran tworzenia playlisty, aktualnych playlist, analizy piosenki
    for widget in root.winfo_children():
        widget.pack_forget()

    # Pokazujemy główny ekran
    label.pack(pady=10, padx=10)
    stworzenie_playlisty.pack(pady=10, padx=10)
    aktualne_playlisty.pack(pady=10, padx=10)
    analiza_piosenki.pack(pady=10, padx=10)

root = tk.Tk()  # inicjalizacja okna
root.title("Interfejs główny")  # tytuł aplikacji

# Etykieta powitalna
main_image = tk.PhotoImage(file="Interfejs_glowny.png")
# Tworzymy Label z obrazkiem
main_image_l = tk.Label(root, image=main_image)
# Zapisujemy referencję do obrazka
main_image_l.image = main_image
# Wyświetlamy obrazek
main_image_l.pack()


label = tk.Label(root, text="Witamy w naszej aplikacji. \nSłuży ona do analizy piosenek\nDostępne opcje:", font=("Arial", 14))
label.pack(pady=10, padx=10)

# Przycisk do tworzenia playlisty
stworzenie_playlisty = tk.Button(root, text="Stworzenie playlisty", font=("Arial", 14), command=lambda: create_playlist(root, label, stworzenie_playlisty, aktualne_playlisty, analiza_piosenki,main_image_l))
stworzenie_playlisty.pack(pady=10, padx=10)

# Pozostałe przyciski
aktualne_playlisty = tk.Button(root, text="Aktualne playlisty", font=("Arial", 14), command=lambda: actual_playlist(root, label, stworzenie_playlisty, aktualne_playlisty, analiza_piosenki, main_image_l))
aktualne_playlisty.pack(pady=10, padx=10)

analiza_piosenki = tk.Button(root, text="Analiza piosenki", font=("Arial", 14), command=lambda: song_analysis(root, label, stworzenie_playlisty, aktualne_playlisty, analiza_piosenki, main_image_l))
analiza_piosenki.pack(pady=10, padx=10)

root.mainloop()
