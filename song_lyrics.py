import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def get_song_lyrics(song_name):
    # Zamiana spacji na "+" w nazwie piosenki, aby pasowała do URL
    song_name = quote(song_name)

    # Tworzenie URL do wyszukiwania piosenki na tekstowo.pl
    url = f"https://www.tekstowo.pl/szukaj,{song_name}.html"
    # print(f"URL wyszukiwania: {url}")

    # Pobranie strony z wynikami wyszukiwania
    response = requests.get(url)

    if response.status_code == 200:
        # Parsowanie HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Znalezienie pierwszego linku w divie o klasie "card-body p-0"
        div = soup.find('div', {'class': 'card-body p-0'})
        if div:
            link = div.find('a')  # Znalezienie pierwszego linku w tym divie
            if link:
                # Ekstrakcja pełnego URL do strony piosenki
                song_page_url = "https://www.tekstowo.pl" + link['href']
                # print(f"Pierwszy link w divie: {song_page_url}")

                # Pobranie strony piosenki
                song_response = requests.get(song_page_url)
                if song_response.status_code == 200:
                    song_soup = BeautifulSoup(song_response.text, 'html.parser')

                    # Próba znalezienia tekstu piosenki w divie o klasie "inner-text"
                    lyrics_div = song_soup.find('div', {'class': 'inner-text'})
                    if lyrics_div:
                        # Usuwanie zbędnych <br> i pozostawianie nowych linii tam, gdzie są one naturalne
                        lyrics = lyrics_div.get_text(separator="\n").strip()
                        return lyrics
                    else:
                        # Jeśli nie znaleziono tekstu w divie "inner-text", sprawdzamy inne miejsca
                        print("Nie znaleziono tekstu w 'inner-text'. Spróbuję innych divów.")
                        other_divs = song_soup.find_all('div', {'class': 'tekst'})
                        if other_divs:
                            lyrics = other_divs[0].get_text(separator="\n").strip()
                            return lyrics
                        else:
                            return "Nie znaleziono tekstu piosenki w żadnym elemencie."
                else:
                    return "Błąd połączenia z stroną piosenki."
            else:
                return "Nie znaleziono linku do piosenki."
        else:
            return "Nie znaleziono wyników wyszukiwania."
    else:
        return "Błąd połączenia z serwerem."
