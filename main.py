import csv
import pandas as pd
from bs4 import BeautifulSoup


def write_to_csv(message):
    #csvfile = csv.writer(open("chatdata.csv", "w"))
    #csvfile.writerow(["date"])
    file = open(message, encoding="utf8")
    soup = BeautifulSoup(file, 'html.parser')


    #dates = soup.findAll('span', {'class' : 'meta'})


    dates = soup.findAll('div', class_ = '_3-94 _2lem')
    for date in dates:
        print(date.get_text())

    #print(soup.get_text())
    # for date in dates:
    #     data = date.contents[0].split(",", 1)
    #     data = data[1].split("at")
    #     data = str(data[0])
    #     data = data.split(",")
    #     data = " ".join(data)
    #     data = data.split(" ")
    #     data = " ".join(data)
    #     csvfile.writerow([data])

def count_messages_bydate():
    df = pd.read_csv('chatdata.csv')
    df.groupby(df.date).size().to_csv("count.csv", header=True)
    ab = pd.read_csv('count.csv')
    ab['date'] = pd.to_datetime(ab.date)
    ab.sort_values('date').to_csv("sorted.csv", header=True)



write_to_csv("messagetest.html")