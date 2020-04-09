from scraper.scraper_1 import Scraper
# from app.db.get_db import

class SandiUpdate(Scraper):

     def sandi_update_all(db, sandi_link):
         sandi_collection = db['sandi_db']
         sandi_collection.delete_many({})
         sandi_dataset_list = Scraper.get_sandi_produts(Scraper.get_soup(sandi_link))
         sandi_collection.insert_many(sandi_dataset_list)

     def sandi_update_prices(db, sandi_link):
         sandi_collection = db['sandi_db']
         sandi_site = Scraper.get_soup(sandi_link)
         products = sandi_site.find_all('offer')
         for prod in products:
             main_list = (str(prod).split('>')[0]).split('\"')
             id = main_list[3]
             aviable = main_list[1]
             instock = main_list[5]
             price = prod.find('price').text
             currencyId = prod.find('currencyId').text
             sandi_collection.find_one_and_update({'id': id}, {'$set': {'aviable': aviable,
                                                                        'instock': instock,
                                                                        'price': price,
                                                                        'currencyId': currencyId}})


     def sandi_brands_update(db, sandi_link, sandi_brands_update_list):
         sandi_collection = db['sandi_db']
         sandi_site = Scraper.get_soup(sandi_link)
         products = sandi_site.find_all('offer')


