import tkinter as tk

def create_playlist(root, label, stworzenie_playlisty, aktualne_playlisty, analiza_piosenki):
    # Ukrywamy główny ekran
    label.pack_forget()
    stworzenie_playlisty.pack_forget()
    aktualne_playlisty.pack_forget()
    analiza_piosenki.pack_forget()

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
root = tk.Tk()  # inicjalizacja okna
root.title("Interfejs główny")  # tytuł aplikacji

# Etykieta powitalna
label = tk.Label(root, text="Witamy w naszej aplikacji. \nSłuży ona do analizy piosenek\nDostępne opcje:", font=("Arial", 14))
label.pack(pady=10, padx=10)

# Przycisk do tworzenia playlisty
stworzenie_playlisty = tk.Button(root, text="Stworzenie playlisty", font=("Arial", 14))
stworzenie_playlisty.pack(pady=10, padx=10)

# Pozostałe przyciski
aktualne_playlisty = tk.Button(root, text="Aktualne playlisty", font=("Arial", 14))
aktualne_playlisty.pack(pady=10, padx=10)

analiza_piosenki = tk.Button(root, text="Analiza piosenki", font=("Arial", 14))
analiza_piosenki.pack(pady=10, padx=10)

root.mainloop()
