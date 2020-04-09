from scraper.scraper_2 import agromat_scraper
from urllib.request import urlopen
from bs4 import BeautifulSoup


class AgromatUpdate:

     def agromat_update_all(db, agromat_link):
         agromat_collection = db['agromat_db']
         agromat_collection.delete_many({})
         agromat_dataset_list = agromat_scraper(agromat_link)
         agromat_collection.insert_many(agromat_dataset_list)

     def agromat_update_prices(db, agromat_link):
         agromat_collection = db['agromat_db']
         with urlopen(agromat_link) as r:
             xml = r.read().decode('utf-8')
             soup = BeautifulSoup(xml, 'xml')
             products = soup.find_all('product')
             for prod in products:
                 Code = prod.find('Code').text
                 Available = prod.find('Available').text
                 RrcPrice = prod.find('RrcPrice').text
                 Status = prod.find('Status').text
                 agromat_collection.find_one_and_update({'Code': Code},
                                                        {'$set': {'Available': Available,
                                                                  'RrcPrice': RrcPrice,
                                                                  'Status': Status}})