# import pymongo
# from pymongo import MongoClient
import pandas as pd
# client = MongoClient()
#
# client = MongoClient('mongodb://romasoya1402:Roma1989Soya@cluster0-shard-00-00-zkewx.mongodb.net:27017,cluster0-shard-00-01-zkewx.mongodb.net:27017,cluster0-shard-00-02-zkewx.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority ')
#
# db = client.b2b
# #count = db['sandi_db'].count()
# sandi_table= db['sandi_db'].find()

# docs = pd.DataFrame(columns=[])
#
# for num, doc in enumerate(sandi_table):
#     # print(y)
#     # pd = pd.Series(y)
#     # print(pd)
#     # break
#     doc["_id"] = str(doc["_id"])
#
#     # get document _id from dict
#     doc_id = doc["_id"]
#
#     # create a Series obj from the MongoDB dict
#     series_obj = pd.Series(doc, name=doc_id )
#
#     # append the MongoDB Series obj to the DataFrame obj
#     docs = docs.append(series_obj)
#
# print(docs)

def read():
    df = pd.read_csv('work.csv', low_memory=False)
    final = list()
    for num in range(len(df)):
        l_f = list()
        l = list(df.iloc[num])
        for x in l:
            l_f.append(str(x))
        while (l_f.count('nan')):
            l_f.remove('nan')
        final.append(l_f)
    return final


