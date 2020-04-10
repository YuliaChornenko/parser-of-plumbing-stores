from pymongo import MongoClient
import pandas as pd


client = MongoClient('mongodb://romasoya1402:Roma1989Soya@cluster0-shard-00-00-zkewx.mongodb.net:27017,cluster0-shard-00-01-zkewx.mongodb.net:27017,cluster0-shard-00-02-zkewx.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.b2b




def connection(table_name):
    client = MongoClient('mongodb://romasoya1402:Roma1989Soya@cluster0-shard-00-00-zkewx.mongodb.net:27017,cluster0-shard-00-01-zkewx.mongodb.net:27017,cluster0-shard-00-02-zkewx.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client.b2b
    table = db[table_name].find()

    return table


def prepare_csv(table_name):
    docs = pd.DataFrame(list(connection(table_name)))
    string = 'app/db/data/' + str(table_name) + '.csv'
    docs = docs.to_csv(string, index = False)



# table = connection('sandi_db')
# docs = pd.DataFrame(list(connection('sandi_db')))
# docs.to_excel('data/test.xlsx',index=None, header=True)
