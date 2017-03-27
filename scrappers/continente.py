#!/usr/bin/python
from lxml import html
import requests
import time
from selenium import webdriver
from pyvirtualdisplay import Display
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from pprint import pprint
import math

url = 'https://www.continente.pt/stores/continente/pt-pt/public/Pages/category.aspx?cat=bio-saudavel(eCsf_WebProductCatalog_MegastoreContinenteOnline_Continente_EUR_Colombo_PT)#/?pl=815'

'''
remove duplicates while preserving order
'''


def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def getNproducts(i):
    anUrl = 'https://www.continente.pt/stores/continente/pt-pt/public/Pages/category.aspx?cat=' + i
    driver = webdriver.Firefox()

    driver.get(anUrl)
    tree = html.fromstring(driver.page_source)
    driver.quit()
    ll = len(tree.xpath('//*[@id]/div/div/div[1]/div/div[1]/span/text()')) - 1
    return tree.xpath('//*[@id]/div/div/div[1]/div/div[1]/span/text()')[ll].strip().replace('(', '').replace(')', '')


def n_products_by_category(tree):
    linklist = tree.xpath('//*[@id]/@id')
    filteredlist = [x for x in linklist if 'eCsf' in x]
    removedDuplicatesList = f7(filteredlist)
    category_nproducts = []

    for i in removedDuplicatesList:
        category_nproducts.append([i, getNproducts(i)])
        time.sleep(10)
    return category_nproducts


def getAllProducts(list):
    x = 0
    connection = MongoClient('mongodb://localhost:27017/')
    db = connection.pyramid
    finalProducts = []
    for i in list:
        for j in range(1, int(math.ceil(int(i[1]) / 20)) + 1):
            if "Campanhas" in i[0]:
                eachUrl = 'https://www.continente.pt/stores/continente/pt-pt/public/Pages/category.aspx?cat=' + \
                    i[0] + '#/?pl=20&page=' + str(j)
                display = Display(visible=0, size=(800, 600))
                display.start()
                driver = webdriver.Firefox()

                driver.get(eachUrl)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
 
                time.sleep(10)
                tree = html.fromstring(driver.page_source)
                names_arr = [name for name in tree.xpath(
                    '//*[@id]/div/div/div/div/div/div/div/div/div/div/div/a/text()') if name.strip()]
            # prices need to be striped
                price_arr = [price for price in tree.xpath(
                    '//*[@id]/div/div/div/div/div/div/div/div/div/div[4]/div[1]/div[1]/text()') if price.strip()]
                print (tree.xpath(
                    '//*[@id]/div/div/div/div/div/div/div/div/div[1]/div[1]/div[1]/a/img/@src'))
                img_href_arr = [href for href in tree.xpath(
                    '//*[@id]/div/div/div/div/div/div/div/div/div[1]/div[1]/div[1]/a/img/@src') if href.strip()]

                for k in range(len(names_arr)):
                    finalProducts.append({"name": names_arr[k], "category": 0, "img": img_href_arr[
                                         k], "price": img_href_arr[k], "promo": True})
                try:
                    result = db.continente.insert_many(
                        finalProducts, ordered=False)
                except BulkWriteError as bwe:
                    pprint(bwe.details)

                # all from this list are in promotion
            # print (len(names_arr))
            # print (len(price_arr))
            # print (len(img_href_arr))
            # print (in_promotion_arr)
            #+=len((filter(lambda name: name.strip(),tree.xpath('//*[@id]/div/div/div/div/div/div/div/div/div/div/div/a/text()'))))
                driver.quit()
                display.stop()
            else:
                eachUrl = 'https://www.continente.pt/stores/continente/pt-pt/public/Pages/category.aspx?cat=' + \
                    i[0] + '#/?pl=20&page=' + str(j)
                #display = Display(visible=0, size=(800, 600))
                #display.start()
                
                driver = webdriver.Firefox()

                driver.get(eachUrl)
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(10)
                tree = html.fromstring(driver.page_source)
                another_tree = tree.xpath(
                    '//*[@id]/div/div/div/div/div/div/div/div')

                names_arr = [name for name in tree.xpath(
                    '//*[@id]/div/div/div/div/div/div/div/div/div/div/div/a/text()') if name.strip()]
            # prices need to be striped
                price_arr = [price for price in tree.xpath(
                    '//*[@id]/div/div/div/div/div/div/div/div/div/div[4]/div[1]/div[1]/text()') if price.strip()]
                img_href_arr = [href for href in tree.xpath(
                    '//*[@id]/div/div/div/div/div/div/div/div/div[1]/div[1]/div[1]/a/img/@src') if href.strip()]

                print (tree.xpath(
                    '//*[@id]/div/div/div/div/div/div/div/div/div[1]/div[1]/div[1]/a/img/@src'))
                for k in (range(len(names_arr))):
                    finalProducts.append({"name": names_arr[k], "category": 0, "img": img_href_arr[
                        k], "price": price_arr[k], "promo": False})
                try:
                    result = db.continente.insert_many(
                        finalProducts, ordered=False)
                except BulkWriteError as bwe:
                    pprint(bwe.details)

            # print (len(names_arr))
            # print (len(price_arr))
            # print (len(img_href_arr))
            # print (in_promotion_arr)
            #+=len((filter(lambda name: name.strip(),tree.xpath('//*[@id]/div/div/div/div/div/div/div/div/div/div/div/a/text()'))))
                driver.quit()
                #display.stop()
    print('closing')
    connection.close()


def loopAllPages(link):
    driver = webdriver.Firefox()

    driver.get(link)
    tree = html.fromstring(driver.page_source)
    driver.quit()
    getAllProducts(n_products_by_category(tree))

loopAllPages(url)