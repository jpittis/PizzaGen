#!flask/bin/python
import requests
from bs4 import BeautifulSoup
import sqlite3

def parseToppings(soup):

    choices = []

    for tag in soup.find_all('h3'):
        choices.append(tag.get_text())

    for i in range(0, len(choices)):
        choices[i] = choices[i].replace('\n', '').replace('\r', '').rstrip().lstrip()
    choices.pop()
    choices.pop(0)

    return choices

def getToppings():
    all_soup = []

    r = requests.get("http://www.pizzapizza.ca/fresh-toppings-bk/meattab/")
    all_soup.append(BeautifulSoup(r.text))
    r = requests.get("http://www.pizzapizza.ca/fresh-toppings-bk/veggietab/")
    all_soup.append(BeautifulSoup(r.text))
    r = requests.get("http://www.pizzapizza.ca/fresh-toppings-bk/saucesanddoughtab/")
    all_soup.append(BeautifulSoup(r.text))
    r = requests.get("http://www.pizzapizza.ca/fresh-toppings-bk/cheesetab/")
    all_soup.append(BeautifulSoup(r.text))

    toppings_lists = []

    for soup in all_soup:
        toppings_lists.append(parseToppings(soup))
    return toppings_lists

if __name__ == '__main__':
    toppings = getToppings()
    db = sqlite3.connect('toppings.db')
    c = db.cursor()
    c.execute('''DROP TABLE IF EXISTS toppings''')
    c.execute('''CREATE TABLE IF NOT EXISTS toppings (
        id INT PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        type TEXT NOT NULL
        )''')
    topping_name = ["meat", "veggies", "sauceanddough", "cheese"]
    for i in range(4):
        for t in toppings[i]:
            c.execute('''INSERT OR REPLACE INTO toppings VALUES (?, ?, ?)''',
                (t, t, topping_name[i]))
    db.commit()
