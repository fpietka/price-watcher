#!/usr/bin/python3

from urllib import request
from bs4 import BeautifulSoup

from sys import stdout


def fetchprices(name, urls):
    stdout.write('-- %s ' % name)
    stdout.flush()
    data = list()
    for url in urls:
        soup = BeautifulSoup(request.urlopen(url).read())

        if name == 'LDLC.com':
            title = soup.find('div', id='productheader').find('h1').find('span', class_='designation_courte').string
            price = float(soup.find('div', id='productheader').find('span', 'prix').find('meta', attrs={'itemprop': 'price'})['content'].replace(',', '.'))
        elif name == 'Materiel.net':
            title_1 = u''.join([s.string for s in soup.find('h1', id='ProdTitle').find('a').find_all(text=True)])[1:-1]
            title_2 = soup.find('h1', id='ProdTitle').find('span', attrs={'itemprop': 'name'}).string
            title = u''.join((title_1, title_2))
            price = float(soup.find('div', class_='Price').find('span', attrs={'property': 'v:price'}).string.replace(',', '.'))

        data.append((title, price))
        stdout.write('.')
        stdout.flush()

    print()
    col_width = max(len(title) for (title, price) in data) + 2
    for title, price in data:
        print(u''.join((title.ljust(col_width), str(price))))

    print()
    print(u' '.join(('total:', str(round(sum([price for (title, price) in data]), 2)))))
    print()


# LDLC.com

urls = [
    'http://www.ldlc.com/fiche/PB00125011.html',
    'http://www.ldlc.com/fiche/PB00148537.html'
]

fetchprices('LDLC.com', urls)

# Materiel.net

urls = [
    'http://www.materiel.net/alimentation-pour-pc/be-quiet-pure-power-l8-530w-72353.html',
    'http://www.materiel.net/processeur-socket-1150/intel-core-i5-4670-89296.html'
]

fetchprices('Materiel.net', urls)
