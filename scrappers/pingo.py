#!/usr/bin/python
from lxml import html
import requests
import time
import json
from pymongo import MongoClient


def loopAllPages(link):
    connection = MongoClient('mongodb://localhost:27017/')
    db = connection.pyramid
    db.pingodoce.drop()
    for i in range(1, 190):
        allProducts = getProducts(link, '' + str(i))
        result = db.pingodoce.insert_many(allProducts)
        # print(aProduct)

        time.sleep(5)
    connection.close()
'''
	first find products ids. we'll need this cause some products are in promotion
	and we'll need id to find which ones
	for each id: retrive name,price,category,imgUrl,promotion? change price
'''


def getProducts(link, page):
    page = requests.get(link + page)
    parsed_json = json.loads(page.content)
    print(parsed_json['rendered_elements'])
    tree = html.fromstring(parsed_json['rendered_elements'])
    this_page_products = []
    products_ids = tree.xpath('//*[@id]/@id')
    for i in products_ids:
        #print ('//*[@id="'+i+'"]/h9/text()')
        product_name = tree.xpath('//*[@id="' + i + '"]/h9/text()')[0].strip()
        product_category = tree.xpath(
            '//*[@id="' + i + '"]/div[2]/text()')[0].strip()
        # //*[@id="post-48046"]/div[1]/div/div/div[1]/div[1]
        product_img = tree.xpath(
            '//*[@id="' + i + '"]/div[1]/img/@src')[0].strip()
        if len(tree.xpath('//*[@id="' + i + '"]/div[1]/div/div/div[2]/text()')) > 0:
            product_price = tree.xpath('//*[@id="' + i + '"]/div[1]/div/div/div[2]/text()')[0].strip(
            ) + '.' + tree.xpath('//*[@id="' + i + '"]/div[1]/div/div/div[1]/div[1]/text()')[0].strip()
            product_promo = True
        else:
            product_price = tree.xpath(
                '//*[@id="' + i + '"]/h6/span/text()')[0].strip()
            product_promo = False
        this_page_products.append(
            {"name": product_name, "category": product_category, "img": product_img, "price": product_price, "promo": product_promo})
    # print(this_page_products)
    return this_page_products

'''
	product_name = tree.xpath('//*[@id]/h9/text()')
	product_category = tree.xpath('//*[@id]/div[2]/text()')
	print (tree.xpath('//*[@id]/div[1]/div/div/div[2]/text()'))
	product_price = tree.xpath('//*[@id]/h6/span/text()')
	print (product_price)
'''
url = 'http://www.pingodoce.pt/wp-content/themes/pingodoce/ajax/pd-ajax.php?action=search_results&limit=12&search_type=product_search&post_type=product&product_settings=marca-propria&pesquisa=&category=&categoria=&tag=&infiniteres=true&offsets=false&pagina='

loopAllPages(url)
