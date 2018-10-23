import csv
import pandas as pd
from bs4 import BeautifulSoup


def write_to_csv(html_input):
    #csvfile = csv.writer(open("chatdata.csv", "w"))
    #csvfile.writerow(["date"])
    file = open(html_input, encoding="utf8")
    soup = BeautifulSoup(file, 'html.parser')

    dates = soup.findAll('div', class_ = '_3-94 _2lem')
    text = soup.findAll('div', class_='_3-96 _2let')
    author = soup.findAll('div', class_='_3-96 _2pio _2lek _2lel')

    for k in range(len(text)):
        print(author[k].get_text())
        print(dates[k+1].get_text())
        print(text[k].get_text())
        print("")

    #reac = soup.findAll('li')
    # print(reac)

    # for date in dates:
    #     data = date.contents[0].split(",", 1)
    #     data = data[1].split("at")
    #     data = str(data[0])
    #     data = data.split(",")
    #     data = " ".join(data)
    #     data = data.split(" ")
    #     data = " ".join(data)
    #     csvfile.writerow([data])

# def count_messages_bydate():
#     df = pd.read_csv('chatdata.csv')
#     df.groupby(df.date).size().to_csv("count.csv", header=True)
#     ab = pd.read_csv('count.csv')
#     ab['date'] = pd.to_datetime(ab.date)
#     ab.sort_values('date').to_csv("sorted.csv", header=True)



write_to_csv("messagetest.html")