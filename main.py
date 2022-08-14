import requests
from http import cookies
from bs4 import BeautifulSoup
import re
import time
import csv


def connection(url):
    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 OPR/89.0.4447.64 (Edition Yx GX) '}

    cookies = dict(cookies_are='working')
    headers = session.headers
    fullpage = requests.get(url, headers=headers, cookies=cookies)
    response = fullpage.headers
    return fullpage


def parse(fullpage):
    soup = BeautifulSoup(fullpage.content, 'html.parser')
    iter = 0
    result = list()
    #< span class ="o_6" > Москва и Московская область < / span >
    sity = soup.find("span", {"class": "o_6"})
    print(sity.text)


    exit = 0
    for pr in soup.findAll("div", {"class": "u_7 vn ss vc", "class": "u_9 vn"}):
        iter = iter + 1
        #< div class ="uK" > Нет в наличии < / div >
        try:
            ex = pr.find("div", {"class": "uK"})
            print(ex.text)
        except:
           pass
        else:
            if ex.text == "Нет в наличии" or ex.text == "Только в розничных магазинах":
                exit = 1
                return exit
        #
        # ссылка
        urlin = pr.find('a')
        url = urlin.get('href')
        #
        # наименование
        namein = pr.find("p", {"class": "RW"})
        name = (namein.text)
        #
        # цена/промоцена
        try:
            pricein = pr.find("p", {"class": "R_6"})
            price = pricein.text
        except:
            pricein = pr.find("span", {"class": "R_8"})
            listInt = list(str(j) for j in range(0, 10))
            price = pricein.text
            priceStr = ''
            for j in price:
                if j in listInt:
                    priceStr = priceStr + j
            salepriceFloat = float(priceStr)
        else:
            listInt = list(str(j) for j in range(0, 10))
            priceStr = ''
            for j in price:
                if j in listInt:
                    priceStr = priceStr + j
            priceFloat = float(priceStr)
        #
        # промо цена
        try:
            pricein = pr.find("p", {"class": "R_6"})
            price = pricein.text
        except:
            pass
        else:
            listInt = list(str(j) for j in range(0, 10))
            price = pricein.text
            priceStr = ''
            for j in price:
                if j in listInt:
                    priceStr = priceStr + j
            salepriceFloat = float(priceStr)
        #
        # id товара
        id = re.search(r'id/', url)
        id = re.sub(r"\D+", "", url)

        # город
        result.append(dict(id = id, title = name, price = priceFloat, promoprice = salepriceFloat, url = url))
        #print(iter, '* ', 'url:', url, 'name:', name, 'price:', priceFloat, 'salePrice:', salepriceFloat, 'id:', id)

    return result

def save(parsepage):
    kol = 1
    for st in parsepage:
        resultst = st.values()
        try:
            with open('msk.csv', 'a+') as csvfile:
                file_write = csv.writer(csvfile)
                file_write.writerow(resultst)
                print('запись успешна', str(kol))
                kol += 1
        except:
            print('ошибка записи')

def main(url):
    urlpage = url
    numpage = 1
    x = 0
    while True:
        response = connection(urlpage)

        parsepage = parse(response)
        if parsepage == 1:
            break
        save(parsepage)
        print(numpage)
        time.sleep(1)
        numpage = numpage + 1
        numpagestr = str(numpage)
        urlpage = url + '/page/' + numpagestr + '/'
        print(urlpage)
        x += 1
    print('parser end')


url = 'https://www.detmir.ru/catalog/index/name/lego'


main(url)

