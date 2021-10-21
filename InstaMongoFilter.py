from pymongo import MongoClient
from pprint import pprint


client = MongoClient('localhost', 27017)
db = client['instagram']
users = db.instagram

name = input('Введите имя пользователя: ')
subscriber = users.count_documents({'$and': [{'user_name': name, 'subscriber_type': 'subscriber'}]})
print(f'-------------------\nПОДПИСЧИКИ: {subscriber}\n-------------------')
for user in users.find({'$and': [{'user_name': name, 'subscriber_type': 'subscriber'}]}):
    pprint(user)
subscription = users.count_documents({'$and': [{'user_name': name, 'subscriber_type': 'subscription'}]})
print(f'-------------------\nПОДПИСКИ: {subscription}\n------------------- ')
for user in users.find({'$and': [{'user_name': name, 'subscriber_type': 'subscription'}]}):
    pprint(user)