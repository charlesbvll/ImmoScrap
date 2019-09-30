from bs4 import BeautifulSoup as bs
from selenium import webdriver
import csv
import os

filename = 'offers.csv'

if os.path.exists(filename):
    os.remove(filename)

headers = ['Type', 'Prix', 'Lieu', 'Quartier', 'Surface',
           'Nb_pieces', 'Nb_chambres', 'Extra', 'Numero', 'Lien']

with open(filename, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(headers)

f.close()

cp = input("Code postal ?\n")
max_page = input("Jusqu a quelle page ?\n")
choice = raw_input("Entrer a pour achat ou l pour location\n")

buy = 'https://www.seloger.com/list.htm?enterprise=0&natures=1,4&places=%5b%7bcp%3a' + \
    str(cp) + '%7d%5d&projects=2&qsversion=1.0&rooms=1,2,3,4&types=1'
rent = 'https://www.seloger.com/list.htm?enterprise=0&furnished=0&places=%5b%7bcp%3a' + \
    str(cp) + '%7d%5d&projects=1&qsversion=1.0&rooms=1,2,3,4&types=1'

if choice.lower() in ['achat', 'a']:
    adress = buy
elif choice.lower() in ['location', 'l']:
    adress = rent

for x in xrange(1, max_page):
    url = adress + '&LISTING-LISTpg=' + str(x)

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    html = browser.page_source
#	browser.close()

    soup = bs(html, "html.parser")

    containers = soup.findAll("div", {"class": ["c-pa-list c-pa-sl c-pa-gold cartouche ",
                                                "c-pa-list c-pa-bd c-pa-gold cartouche ", "c-pa-list c-pa-sl c-pa-silver cartouche ",
                                                "c-pa-list c-pa-bd c-pa-silver cartouche ", "c-pa-list c-pa-sl cartouche "]})

    for c in containers:
        info_c = c.findAll("div", {"class": "c-pa-info"})[0]

        h_link = info_c.a["href"].strip()
        h_quartier = h_link.split('/')[-2].replace('-', ' ')
        if 'paris' in h_quartier:
            h_quartier = h_link.split('/')[-1].replace('-', ' ')
        if '?' in h_quartier:
            h_quartier = ''

        h_type = info_c.a.text
        h_price = info_c.findAll(
            "span", {"class": "c-pa-cprice"})[0].text.strip().encode('ascii', errors='ignore')
        h_loc = info_c.findAll("div", {
                               "class": "c-pa-city"})[0].text.encode('ascii', errors='ignore').replace('me', '')
        if len(info_c.findAll("a", {"class": " tagClick desktop listContactPhone"})) != 0:
            h_phone = info_c.findAll("a", {"class": " tagClick desktop listContactPhone"})[
                0]["data-tooltip-focus"]

        h_nbp = ""
        h_nbch = ""
        h_extra = ""
        h_surface = ""

        print(h_type)
        print(h_price)
        print(h_loc)
        print(h_quartier)

        for info in info_c.div.text.strip().split('\n'):
            if "m" in info:
                h_surface = info.encode(
                    'ascii', errors='ignore').replace(' m', '')
                print(h_surface)
            elif "p" in info:
                h_nbp = info.replace(' p', '')
                print(h_nbp)
            elif "ch" in info:
                h_nbch = info.replace(' ch', '')
                print(h_nbch)
            else:
                h_extra = info.encode('ascii', errors='ignore')
                print(h_extra)
        print(h_phone)
        print("")

        with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([h_type, h_price, h_loc, h_quartier,
                             h_surface, h_nbp, h_nbch, h_extra, h_phone, h_link])

        f.close()
