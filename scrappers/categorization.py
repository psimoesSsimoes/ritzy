from pymongo import MongoClient
import sys

reload(sys)
sys.setdefaultencoding('utf8')


category = []
products = []

# with case insensitivity


f = open('subcat_prod.txt', 'r')
for line in f:
    category.append(line.split(':')[0])
    products.append(line.split(':')[1].split(','))
print(category)
print(products)


connection = MongoClient('mongodb://localhost:27017/')
db = connection.pyramid
cursor = db.pingodoce.find()
for item in cursor:
    for p in range(len(products)):
        for i in products[p]:
            if i.lower() in item['name'].lower():
                db.pingodoce.update_one({
                    '_id': item['_id']
                },
                    {'$set': {'subcat': category[p]}

                     })
