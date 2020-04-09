from pymongo import MongoClient
from update_function.sandi_update import SandiUpdate
from update_function.antey_update import AnteyUpdate
from update_function.agromat_update import AgromatUpdate
from scraper.site_links import sandi_link, antey_link, agromat_link


cluster = MongoClient("mongodb://romasoya1402:Roma1989Soya@cluster0-shard-00-00-zkewx.mongodb.net:27017,cluster0-shard-00-01-zkewx.mongodb.net:27017,cluster0-shard-00-02-zkewx.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")

db = cluster['b2b']

# полностью обновляют
# SandiUpdate.sandi_update_all(db, sandi_link)
AnteyUpdate.antey_update_all(db, antey_link)
# AgromatUpdate.agromat_update_all(db, agromat_link)

# обновляют цену, наличие
# SandiUpdate.sandi_update_prices(db, sandi_link)
# AnteyUpdate.antey_update_prices(db, antey_link)
# AgromatUpdate.agromat_update_prices(db, agromat_link)