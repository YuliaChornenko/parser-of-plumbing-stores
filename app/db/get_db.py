from pymongo import MongoClient
import pandas as pd


client = MongoClient('mongodb://romasoya1402:Roma1989Soya@cluster0-shard-00-00-zkewx.mongodb.net:27017,cluster0-shard-00-01-zkewx.mongodb.net:27017,cluster0-shard-00-02-zkewx.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.b2b

def prepare_csv(table_name):
    client = MongoClient('mongodb://romasoya1402:Roma1989Soya@cluster0-shard-00-00-zkewx.mongodb.net:27017,cluster0-shard-00-01-zkewx.mongodb.net:27017,cluster0-shard-00-02-zkewx.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client.b2b
    sandi_table= db[table_name].find()
    docs = pd.DataFrame(columns=[])
    for num, doc in enumerate(sandi_table):
        doc["_id"] = str(doc["_id"])
        series_obj = pd.Series(doc)
        docs = docs.append(series_obj, ignore_index=True )

    string = 'app/db/data/' + str(table_name) + '.csv'
    string1 = 'app/db/data/' + str(table_name) + '.xlsx'
    docs = docs.to_csv(string, index = False)
    docs = pd.read_csv(string)
    docs.to_excel(string1, index=None, header=True)

# print(docs)
# g=0
# def read(g):
#     df = pd.read_csv('work.csv', low_memory=False)
#     category = list(df.columns)
#     final = list()
#     for num in range(len(df)):
#         l_f = list()
#         l = list(df.iloc[1])
#         for x in l:
#             l_f.append(str(x))
#         list_pos = list()
#         i = 0
#         for nan in l_f:
#             if nan == 'nan':
#                 list_pos.append(i)
#             i += 1
#         while (l_f.count('nan')):
#             l_f.remove('nan')
#         n=0
#         print(list_pos)
#         for x in list_pos:
#             x = x-n
#             print(x)
#             if len(category) == x:
#                 break
#             a = category.pop(x)
#             print(category)
#             print(len(category))
#             print(len(l_f))
#             n+=1
#
#         d_f = dict(zip(category, l_f))
#         final.append(l_f)
#         g+=1
#     return final
#
# read(g)

def read(file):
    df = pd.read_csv(file, low_memory=False)
    category = list(df.columns)
    final = list()
    for i in range(len(df)):
        l = df.iloc[i]
        l_f = list()
        for x in l:
            l_f.append([str(x)])
        d_f = dict(zip(category, l_f))
        for cat in category:
            if d_f[cat] == ['nan']:
                d_f.pop(cat)
        final.append(d_f)
    return final[:6]


# prepare_csv('antey_db')


def connection(table_name):
    client = MongoClient(
        'mongodb://romasoya1402:Roma1989Soya@cluster0-shard-00-00-zkewx.mongodb.net:27017,cluster0-shard-00-01-zkewx.mongodb.net:27017,cluster0-shard-00-02-zkewx.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client.b2b
    table = db[table_name].find()
    print(table)
    return table



def prepare_csv(table_name, table):
    docs = pd.DataFrame(columns=[])
    for num, doc in enumerate(table):
        doc["_id"] = str(doc["_id"])
        series_obj = pd.Series(doc)
        docs = docs.append(series_obj, ignore_index=True )
    string = 'app/db/data/' + str(table_name) + '.csv'
    string1 = 'app/db/data/' + str(table_name) + '.xlsx'
    docs = docs.to_csv(string, index = False)
    docs = pd.read_csv(string)
    docs.to_excel(string1, index=None, header=True)

