from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId

def get_database():
    CONNECTION_STRING=r'mongodb+srv://admin:admin@cluster0.x24cglf.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(CONNECTION_STRING)
    return client['User_list']

dbname = get_database()
collection= dbname["test"]

# Insert
# collection.insert_one({'name':'Jack','scores':100})
#collection.insert_many([{'name':'Jack','scores':100},{'name':'May','scores':90}])

#find
# name='Ja'
# email='pq125uty77jr100@gmail.com'
# password='1qaz'
# result=collection.find_one({'$or':[{'name':name},{'email':email}]})
# if result is not None:
#     print(result['password'])
# else:
#     print('error')

#update
#collection.update_many({'name':'May'},{'$set':{'score':200}})

#delete
# collection.delete_many({'name':'Jack'})
# id='63d3466950731da87e258387'
# objInstance=ObjectId(id)
# cursor=list(collection.find({'_id':objInstance}))
cursor=list(collection.find({'name':'May'}))
for i,c in enumerate(cursor):
    del c['_id'],c['scores']
    print(i,c)
print(cursor)

