from scraper.scraper_1 import Scraper
# from app.db.get_db import
from celery import Celery

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
         for prod in products:
             if prod.find('param') != None:
                 prod_param = prod.find_all('param')
                 for param in prod_param:
                     param_category = (str(param).split('\"')[1]).replace('.', '')
                     param = param.text
                     if param_category == 'Бренд':
                         if param in sandi_brands_update_list:
                             main_list = (str(prod).split('>')[0]).split('\"')
                             id = main_list[3]
                             aviable = main_list[1]
                             instock = main_list[5]
                             name = prod.find('name').text
                             delivery = prod.find('delivery').text
                             vendor = prod.find('vendor').text
                             vendorCode = prod.find('vendorCode').text
                             model = prod.find('model').text
                             description = prod.find('description').text
                             price = prod.find('price').text
                             currencyId = prod.find('currencyId').text
                             categoryId = prod.find('categoryId').text
                             sandi_dataset = {
                                 'id': id,
                                 'name': name,
                                 'aviable': aviable,
                                 'instock': instock,
                                 'price': price,
                                 'currencyId': currencyId,
                                 'delivery': delivery,
                                 'vendor': vendor,
                                 'vendorCode': vendorCode,
                                 'model': model,
                                 'description': description,
                                 'categoryId': categoryId,
                             }
                             if prod.find('param') != None:
                                 prod_param = prod.find_all('param')
                                 for param in prod_param:
                                     param_category = (str(param).split('\"')[1]).replace('.', '')
                                     param = param.text
                                     sandi_dataset[param_category] = param

                             update = sandi_collection.find_one_and_update({'id': id},
                                                                           {'$set': sandi_dataset})
                             if update == None:
                                 sandi_collection.insert_one(sandi_dataset)
