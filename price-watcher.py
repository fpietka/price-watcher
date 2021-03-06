#!/usr/bin/python3

from urllib import request, error
from bs4 import BeautifulSoup

from sys import stdout



class Watcher():
    def __init__(self, name):
        try:
            self.adapter = eval(name)()
        except NameError:
            raise Exception('No adapter for "%s"' % name)
        self.name = name

    def fetchprices(self, urls):
        stdout.write('-- %s ' % self.name)
        stdout.flush()
        data = list()
        for url in urls:
            try:
                soup = BeautifulSoup(request.urlopen(url).read())
                data.append(self.adapter.fetch(soup))
            except TimeoutError:
                data.append(('%s (%s)' % (url, 'timeout'), 0))
            except error.URLError as e:
                if hasattr(e, 'code'):
                    data.append(('%s (%s)' % (url, e.code), 0))
                else:
                    data.append(('%s (%s)' % (url, 'wrong url'), 0))
            stdout.write('.')
            stdout.flush()

        print()
        col_width = max(len(title) for (title, price) in data) + 2
        for title, price in data:
            print(u''.join((title.ljust(col_width), str(price))))

        print()
        print(u' '.join(('total:', str(round(sum([price for (title, price) in data]), 2)))))
        print()


class Adapter():
    def fetch(self, soup):
        if type(soup) is not BeautifulSoup:
            raise Exception('Wrong type for parameter. Type is %s but bs4.BeautifulSoup was expected' % type(soup))


class Ldlc(Adapter):
    def fetch(self, soup):
        super().fetch(soup)
        title = soup.find('div', id='productheader').find('h1').find('span', class_='designation_courte').string
        price = float(soup.find('div', id='productheader').find('span', 'prix').find('meta', attrs={'itemprop': 'price'})['content'].replace(',', '.'))
        return (title, price)


class Materiel(Adapter):
    def fetch(self, soup):
        super().fetch(soup)
        title_1 = u''.join([s.string for s in soup.find('h1', id='ProdTitle').find('a').find_all(text=True)])[1:-1]
        title_2 = soup.find('h1', id='ProdTitle').find('span', attrs={'itemprop': 'name'}).string
        title = u''.join((title_1, title_2))
        price = float(soup.find('div', class_='Price').find('span', attrs={'property': 'v:price'}).string.replace(',', '.').split(' ')[0])
        return (title, price)


# LDLC.com

urls = [
    'http://www.ldlc.com/fiche/PB00125011.html',
    'http://www.ldlc.com/fiche/PB00148537.html'
]

watcher = Watcher('Ldlc')
watcher.fetchprices(urls)

# Materiel.net

urls = [
    'http://www.materiel.net/alimentation-pour-pc/be-quiet-pure-power-l8-530w-72353.html',
    'http://www.materiel.net/processeur-socket-1150/intel-core-i5-4670-89296.html'
]

watcher = Watcher('Materiel')
watcher.fetchprices(urls)
