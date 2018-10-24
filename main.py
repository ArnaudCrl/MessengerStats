import csv
import pandas as pd
from bs4 import BeautifulSoup


def write_to_csv(html_input):
    csvfile = csv.writer(open("tableur.csv", "w",encoding='utf-8', newline=""), delimiter=' ', quotechar='|')
    file = open(html_input, encoding="utf8")
    soup = BeautifulSoup(file, 'lxml')

    dates_raw = soup.findAll('div', class_ = '_3-94 _2lem')
    text_raw = soup.findAll('div', class_='_3-96 _2let')
    author_raw = soup.findAll('div', class_='_3-96 _2pio _2lek _2lel')

    authors = []
    dates = []
    messages = []

    for k in range(len(author_raw)):
        print(k)
        authors.append(author_raw[k].get_text())
        dates.append(dates_raw[k+1].get_text())
        messages.append( text_raw[k].get_text())

    for k in range(len(authors)):
        csvfile.writerow([dates[k], authors[k], messages[k]])

    file.close()

write_to_csv("messagetest.html")