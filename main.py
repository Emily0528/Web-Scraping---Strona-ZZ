from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from bs4 import BeautifulSoup
import requests

from datetime import datetime, timedelta
import datetime
import random
from urllib.parse import urljoin


app = Flask(__name__)
app.secret_key = "x"
app.permanent_session_lifetime = timedelta(minutes=5) # 5 minutowa sesja

# do scrapingu
def get_quotes_and_authors():
    page_scrap = requests.get("http://quotes.toscrape.com")
    soup = BeautifulSoup(page_scrap.text, "html.parser")
    quotes = soup.findAll("span", attrs={"class": "text"})[:5]
    authors = soup.findAll("small", attrs={"class": "author"})[:5]
   
    quotes_list = []
    for quote, author in zip(quotes, authors):
        quotes_list.append((quote.text, author.text))
   
    return quotes_list




# smieszne zagadki
current_puzzle = None
last_update = None

def get_random_puzzle():
    # Pobierz cytat z określonej strony internetowej
    url = "https://webfun.pl/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    card_bodies = soup.find_all("div", class_="card-body")
    random_card_body = random.choice(card_bodies)

    puzzle = random_card_body.find("p", class_="card-text")
    return puzzle.text.strip() if puzzle else "Brak tekstu"

def get_puzzles_and_buttons():
    global current_puzzle
    global last_update

    # Sprawdź, czy minęło 24 godziny od ostatniej aktualizacji
    if last_update is None or (datetime.datetime.now() - last_update).total_seconds() >= 86400:
        current_puzzle = get_random_puzzle()
        last_update = datetime.datetime.now()

    # Zwróć aktualny cytat
    return [(current_puzzle)]


def get_puzzles():
    # Pobieranie strony
    url = "https://webfun.pl/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Znalezienie wszystkich elementów <div> z klasą "card-body"
    card_bodies = soup.find_all("div", class_="card-body")
    
    puzzles = []
    for card_body in card_bodies:
        # Znalezienie elementu <p> z klasą "card-text" wewnątrz <div class="card-body">
        puzzle_long = card_body.find("p", class_="card-text")
        if puzzle_long:
            puzzle_text = puzzle_long.text.strip()
        else:
            puzzle_text = "Brak tekstu"

        
        
        puzzles.append((puzzle_text))
    
    return puzzles



def scrape_birthday_wishes():
    page_scrap = requests.get("https://www.weekendowo.pl/zyczenia/urodziny/smieszne")
    soup = BeautifulSoup(page_scrap.text, "html.parser")
    
    wish_divs = soup.find_all('div', class_='wish bck')
    wishes = []
    for div in wish_divs:
        title = div.find('h3').text.strip()
        paragraph = div.find('p').text.strip()
        clean_text = div.find('div', class_='clean-text').text.strip()

        wish = {
            'title': title,
            'paragraph': paragraph,
            'clean_text': clean_text
        }
        
        wishes.append(wish)

    return wishes
'''
z tym działa
def get_days_to_end_of_year():
    page_scrap = requests.get("https://kalendarzdni.pl/ile-dni-do-konca-roku")
    soup = BeautifulSoup(page_scrap.text, "html.parser")
    paragraph = soup.find('div', class_='col-sm-9').find('p')
    days_left = paragraph.find('b').text.strip()

    return days_left'''



'''
def get_days_info():
    url = "https://kalendarzdni.pl/ile-dni-do-konca-roku"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    col_div = soup.find('div', class_='col-sm-9')
    days_left_paragraph = col_div.find('p', text=lambda t: 'Do końca roku pozostało' in t)
    current_day_paragraph = col_div.find('p', text=lambda t: 'Aktualnie trwa' in t)

    days_left = days_left_paragraph.find('b').text.strip() if days_left_paragraph else "Nie można znaleźć liczby dni"
    current_day = current_day_paragraph.find('b').text.strip() if current_day_paragraph else "Nie można znaleźć aktualnego dnia"

    return current_day, days_left
'''
'''
def get_days_info():
    url = "https://kalendarzdni.pl/ile-dni-do-konca-roku"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    col_div = soup.find('div', class_='col-sm-9')
    if col_div:
        days_left_paragraph = col_div.find('p', text=lambda t: t and 'Do końca roku pozostało' in t)
        current_day_paragraph = col_div.find('p', text=lambda t: t and 'Aktualnie trwa' in t)

        days_left = days_left_paragraph.find('b').text.strip() if days_left_paragraph else "Nie można znaleźć liczby dni"
        current_day = current_day_paragraph.find('b').text.strip() if current_day_paragraph else "Nie można znaleźć aktualnego dnia"
    else:
        days_left = "Nie można znaleźć liczby dni"
        current_day = "Nie można znaleźć aktualnego dnia"

    return current_day, days_left
działa ale brak wartości
def get_days_info():
    url = "https://kalendarzdni.pl/ile-dni-do-konca-roku"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    col_div = soup.find('div', class_='col-sm-9')
    if col_div:
        days_left_paragraph = col_div.find('p', text=lambda t: t and 'Do końca roku pozostało' in t)

        days_left = int(days_left_paragraph.find('b').text.strip()) if days_left_paragraph else None
        total_days_in_year = 366 if datetime.datetime.now().year % 4 == 0 else 365
        current_day = total_days_in_year - days_left if days_left else None
    else:
        days_left = "Nie można znaleźć liczby dni"
        current_day = "Nie można znaleźć aktualnego dnia"

    return current_day, days_left
'''
def get_days_info():
    page_scrap = requests.get("https://kalendarzdni.pl/ile-dni-do-konca-roku")
    soup = BeautifulSoup(page_scrap.text, "html.parser")
    paragraph = soup.find('div', class_='col-sm-9').find('p')
    days_left = int(paragraph.find('b').text.strip())
    total_days_in_year = 366 if datetime.datetime.now().year % 4 == 0 else 365
    current_day = total_days_in_year - days_left 

    return days_left, current_day

@app.route("/") 
def home():
    puzzles_and_buttons = get_puzzles_and_buttons()
    puzzles = get_puzzles()
    current_day, days_left = get_days_info()
    return render_template("index.html", active_page='home', puzzles_and_buttons=puzzles_and_buttons, puzzles=puzzles, current_day=current_day, days_left=days_left)
'''
z tym działa
@app.route("/") 
def home():
    puzzles_and_buttons = get_puzzles_and_buttons()
    puzzles = get_puzzles()
    days_left = get_days_to_end_of_year()
    return render_template("index.html", active_page= 'home', puzzles_and_buttons=puzzles_and_buttons,puzzles=puzzles, value="wartość", days_left=days_left)
    '''


'''
@app.route("/") 
def home():
    puzzles_and_buttons = get_puzzles_and_buttons()
    puzzles = get_puzzles()
    current_day, days_left = get_days_info()
    return render_template("index.html", active_page= 'home', puzzles_and_buttons=puzzles_and_buttons,puzzles=puzzles, value="wartość", current_day=current_day, days_left=days_left)'''

@app.route('/text')
def text():
    puzzles = get_puzzles()
    return render_template('text.html', puzzles=puzzles, active_page='text')

@app.route("/zyczenia")
def zyczenia():
    birthday_wishes = scrape_birthday_wishes()
    return render_template("zyczenia.html", active_page= 'zyczenia', birthday_wishes=birthday_wishes)

if __name__== "__main__": 
    app.run(debug=True)
    
