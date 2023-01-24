from pymongo import MongoClient
import pymongo

def get_database():
    CONNECTION_STRING=r'mongodb+srv://admin:admin@cluster0.x24cglf.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(CONNECTION_STRING)
    return client['User_list']

dbname = get_database()
collection= dbname["data"]

# Insert
# collection.insert_one({'name':'Jack','scores':100})
# collection.insert_many([{'name':'Jack','scores':100},{'name':'Jack','scores':90}])

name='Ja'
email='pq125uty77jr100@gmail.com'
password='1qaz'
result=collection.find_one({'$or':[{'name':name},{'email':email}]})
if result is not None:
    print(result['password'])
else:
    print('error')

