#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml import html
import requests
import time
import json
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import sys
from imp import reload
import random
from random import randint
reload(sys)
sys.setdefaultencoding('utf8')
useragents = ["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:35.0) Gecko/20100101 Firefox/35.0", "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36", "Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36", "Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4", "Mozilla/5.0 (Windows NT 6.1; rv:35.0) Gecko/20100101 Firefox/35.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:35.0) Gecko/20100101 Firefox/35.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36", "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36", "Mozilla/5.0 (Windows NT 5.1; rv:35.0) Gecko/20100101 Firefox/35.0", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36", "Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/7.1.2 Safari/537.85.11", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/7.1.3 Safari/537.85.12", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36", "Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4", "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0", "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36",
              "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/39.0.2171.65 Chrome/39.0.2171.65 Safari/537.36", "Mozilla/5.0 (X11; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0", "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:35.0) Gecko/20100101 Firefox/35.0", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.1.25 (KHTML, like Gecko) QuickLook/5.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/6.1.6 Safari/537.78.2", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0", "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:35.0) Gecko/20100101 Firefox/35.0", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36", "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko) Version/5.1.9 Safari/534.59.10", "Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B411 Safari/600.1.4", "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0) Gecko/20100101 Firefox/34.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10", "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36", "Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53", "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A405 Safari/600.1.4", "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0", "Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0", "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36", "Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.4.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.3 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.3"]
categories = ['http://www.saborintenso.com/chef/caderno-1/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-9/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-19/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-30/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-25/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-41/', 'http://www.saborintenso.com/chef/caderno-42/&ver=tudo/',
              'http://www.saborintenso.com/chef/caderno-45/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-49/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-57/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-54/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-62/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-76/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-66/', 'http://www.saborintenso.com/chef/caderno-84/&ver=tudo/']

keywords_after = ['colher de sopa bem cheia de', 'colher de sopa de', 'colheres de sopa',
                  'colher de café de', 'bifes de', 'bife de', 'peito de', 'folhas de', 'lombos de', 'lombo de' 'de um' 'de']
keywords_toDelete = ['q.b.', 'q.b']
keywords_to_retains_only = ['alho', 'cebola', 'cravinho', 'whiskey', 'brandy', 'alho fran', 'maracuj', 'malagueta', 'pimento', 'cenouras', 'milho', 'louro', 'Noz-moscada', 'frango', 'azeite', 'tomate',
                            'chouriço', 'bacon', 'cenoura', 'caldo', 'esparguete', 'natas', 'queijo', 'sal', 'manteiga', 'limão', 'leite', 'noz-moscada', 'ovo', 'açúcar', 'coco', 'frutos vermelhos', 'amêndoa', 'aveia']


def calculateNumberOfPages(tree):
    last_page = tree.xpath(
        '/html/body/div[3]/div/table/tr/td/a/@href')
    print(last_page[-1].split("page=", 1)[1])
    return int(last_page[-1].split("page=", 1)[1])


def extractIngredientsAndPrep(list):
    ingredients = []
    preparacoes = []
    for w in list:
        print(w)
        headers = {
            'User-Agent': random.choice(useragents),
            'Connection': 'close'
        }
        time.sleep(randint(10, 75))
        page = requests.get(w, headers=headers)
        tree = html.fromstring(page.content)
        ingredients.append(tree.xpath('//*[@id]/ul/li/text()'))
        alltext = tree.xpath('//*[@id]/text()')
        for i in range(len(alltext)):
            if "\n1." in alltext[i]:
                j = i
                preparacao = []
                for x in range(j, len(alltext)):
                    if "\nA equipa do SaborIntenso.com deseja-lhe um bom apetite!" not in alltext[x]:
                        preparacao.append(alltext[x])
                    else:
                        preparacoes.append(preparacao)
                        break
        time.sleep(randint(10, 85))
    return [ingredients, preparacoes]


def getIngredientsForMobile(aList):
    sorted_list = sorted(keywords_to_retains_only, key=len, reverse=True)
    anotherList = []
    for i in aList:
        for k in range(len(keywords_after)):
            if keywords_after[k].lower() in i.lower():
                i = i.replace(keywords_after[k], ' ')
        for j in range(len(sorted_list)):
            if sorted_list[j].lower() in i.lower():
                anotherList.append(sorted_list[j])
                break

    return anotherList


def loopAllCategories():
    connection = MongoClient('mongodb://localhost:27017/')
    db = connection.ritzy
    random.shuffle(categories)
    for i in categories:
        print(i)
        headers = {
            'User-Agent': random.choice(useragents),
            'Connection': 'close'
        }
        page = requests.get(i, headers=headers)  # X-Forwarded-For: 192.168.0.2
        time.sleep(randint(10, 55))
        tree = html.fromstring(page.content)
        category = tree.xpath(
            '/html/body/div[3]/table/tr/td[1]/div/span/text()').pop()
	print(category)
        for a in range(1, calculateNumberOfPages(tree)):
            recipe_name = tree.xpath('//*[@id]/div/p[2]/a/text()')
            recipe_img = tree.xpath('//*[@id]/div/a/img/@src')
            ingredientsAndPrep = extractIngredientsAndPrep(
                tree.xpath('//*[@id]/div/p[2]/a/@href'))
            print("atum")
            print(len(recipe_name))
            print(len(recipe_img))
            print(len(ingredientsAndPrep[0]))
            print(len(ingredientsAndPrep[1]))
            finalRecipes = []
            for k in range(len(recipe_name)):
                print(recipe_name[k])
                print(getIngredientsForMobile(ingredientsAndPrep[0][k]))
                finalRecipes.append({"category": category, "name": recipe_name[k], "img": recipe_img[
                                    k], "ingredients_recipe": getIngredientsForMobile(ingredientsAndPrep[0][k]), "prep": ingredientsAndPrep[1][k]})
                try:
                    result = db.saborintenso.insert_many(
                      (r for r in finalRecipes), ordered=False)
                except BulkWriteError as bwe:
                    pprint(bwe.details)
            finalRecipes = []
            time.sleep(randint(10, 40))

f = open('filter.txt', 'r')
for line in f:
    keywords_to_retains_only += line.split(':')[1].split(',')


loopAllCategories()
