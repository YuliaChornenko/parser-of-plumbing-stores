from pymongo import MongoClient

cluster = MongoClient("mongodb://romasoya1402:Roma1989Soya@cluster0-shard-00-00-zkewx.mongodb.net:27017,cluster0-shard-00-01-zkewx.mongodb.net:27017,cluster0-shard-00-02-zkewx.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")

test_db = cluster['test']

test_collection = test_db['test']

# test_list = [{'id': 3748, 'name': 'egrht', 'land': 'dgf'}, {'id': 374248, 'name': 'fgg', 'fine': 'dgfdg'}]
# test_collection.insert_many(test_list)
# results = test_collection.find_one_and_update
results = test_collection.find_one_and_update({"id":3748}, {"$set": {"name":"key1", 'fgg': '0'}})
print(results)
# print(test_collection.users.find({id: '374sdfghtfyg248'}))
# if 3748 in test_db.test_collection.find({'id': }):
#     print('true')