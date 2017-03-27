#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml import html
import requests
import time
import json
from pymongo import MongoClient
import sys

reload(sys)
sys.setdefaultencoding('utf8')

categories = ['http://www.saborintenso.com/chef/caderno-1/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-9/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-19/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-30/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-25/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-41/', 'http://www.saborintenso.com/chef/caderno-42/&ver=tudo/',
              'http://www.saborintenso.com/chef/caderno-45/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-49/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-57/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-54/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-62/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-76/&ver=tudo/', 'http://www.saborintenso.com/chef/caderno-66/', 'http://www.saborintenso.com/chef/caderno-84/&ver=tudo/']

keywords_after = ['colher de sopa bem cheia de', 'colher de sopa de', 'colheres de sopa','colher de café de', 'bifes de', 'bife de', 'peito de', 'folhas de', 'lombos de', 'lombo de' 'de um' 'de']
keywords_toDelete = ['q.b.', 'q.b']
keywords_to_retains_only = ['alho', 'cebola','cravinho','whiskey','brandy', 'alho fran','maracuj', 'malagueta', 'pimento', 'cenouras', 'milho', 'louro', 'Noz-moscada', 'frango', 'azeite', 'tomate', 'chouriço', 'bacon', 'cenoura', 'caldo', 'esparguete', 'natas', 'queijo', 'sal', 'manteiga', 'limão', 'leite', 'noz-moscada', 'ovo', 'açúcar', 'coco', 'frutos vermelhos', 'amêndoa', 'aveia']


def calculateNumberOfPages(tree):
    last_page = tree.xpath(
        '/html/body/div[3]/div/table/tr/td/a/@href')
    print (last_page[-1].split("page=", 1)[1])
    return int(last_page[-1].split("page=", 1)[1])


def extractIngredientsAndPrep(list):
    ingredients = []
    preparacoes = []
    for w in list:
        page = requests.get(w)
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
    return [ingredients, preparacoes]


def getIngredientsForMobile(aList):
    sorted_list = sorted(keywords_to_retains_only, key=len,reverse=True)
    anotherList=[]
    for i in aList:
        for k in range(len(keywords_after)):
            if keywords_after[k].lower() in i.lower():
               i=i.replace(keywords_after[k], ' ')
        for j in range(len(sorted_list)):
            if sorted_list[j].lower() in i.lower():
                anotherList.append(sorted_list[j])
                break

    return anotherList


def loopAllCategories():
    connection = MongoClient('mongodb://localhost:27017/')
    db = connection.ritzy
    for i in categories:
        page = requests.get(i)
        tree = html.fromstring(page.content)
        category = tree.xpath(
            '/html/body/div[3]/table/tr/td[1]/div/span/text()').pop()
        for a in range(1, calculateNumberOfPages(tree)):
            recipe_name = tree.xpath('//*[@id]/div/p[2]/a/text()')
            recipe_img = tree.xpath('//*[@id]/div/a/img/@src')
            ingredientsAndPrep = extractIngredientsAndPrep(
                tree.xpath('//*[@id]/div/p[2]/a/@href'))
            print(len(recipe_name))
            print(len(recipe_img))
            print(len(ingredientsAndPrep[0]))
            print(len(ingredientsAndPrep[1]))
            finalRecipes = []
            for k in range(len(recipe_name)):
                print(recipe_name[k])
                print(getIngredientsForMobile(ingredientsAndPrep[0][k]))
            #     finalRecipes.append({"category": category, "name": recipe_name[k], "img": recipe_img[
            #                          k], "ingredients_recipe": ingredientsAndPrep[0][k], "prep": ingredientsAndPrep[1][k]})
            # try:
            #     result = db.saborintenso.insert_many(
            #         finalRecipes, ordered=False)
            # except BulkWriteError as bwe:
            #     pprint(bwe.details)
            finalRecipes = []
        print(i)

f = open('filter.txt', 'r')
for line in f:
    keywords_to_retains_only+=line.split(':')[1].split(',')


loopAllCategories()
