import pymongo


client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client["mydatabase"]
user_info = db['users']


test_data = {
    'username': 'amongus',
    'password': 'imposter123'
}


user_info.insert_one(test_data)
found = user_info.find_one({'username': 'amongus'}) 
if found:
    print('yes')