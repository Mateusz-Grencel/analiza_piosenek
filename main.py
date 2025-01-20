import tkinter as tk

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
