from pymongo import MongoClient
from scraper.scraper_1 import Scraper
from scraper.scraper_2 import agromat_scraper
from scraper.site_links import sandi_link, antey_link, agromat_link


cluster = MongoClient("mongodb://romasoya1402:Roma1989Soya@cluster0-shard-00-00-zkewx.mongodb.net:27017,cluster0-shard-00-01-zkewx.mongodb.net:27017,cluster0-shard-00-02-zkewx.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")

# sandi_dataset_list = Scraper.get_sandi_produts(Scraper.get_soup(sandi_link))
# antey_dataset_list = Scraper.get_antey_products(Scraper.get_soup(antey_link))
# agromat_dataset_list = agromat_scraper(agromat_link)

db = cluster['b2b']

# sandi_collection = db['sandi_db']

# antey_collection = db['antey_db']
# agromat_collection = db['agromat_db']
#
# sandi_collection.insert_many(sandi_dataset_list)
# antey_collection.insert_many(antey_dataset_list)
# agromat_collection.insert_many(agromat_dataset_list)
