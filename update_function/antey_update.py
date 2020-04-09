from scraper.scraper_1 import Scraper


class AnteyUpdate(Scraper):

     def antey_update_all(db, antey_link):
         antey_collection = db['antey_db']
         antey_collection.delete_many({})
         antey_dataset_list = Scraper.get_antey_products(Scraper.get_soup(antey_link))
         antey_collection.insert_many(antey_dataset_list)

     def antey_update_prices(db, antey_link):
         antey_collection = db['antey_db']
         antey_site = Scraper.get_soup(antey_link)
         products = antey_site.find_all('product')
         for prod in products:
             product_sku = prod.find('product_sku').text
             product_status = prod.find('product_status').text
             product_price = prod.find('product_price').text
             product_currency = prod.find('product_currency').text
             product_price_online = prod.find('product_price_online').text
             product_price_currency_online = prod.find('product_price_currency_online').text
             sourcePrice = prod.find('sourcePrice').text
             sourceCurrency = prod.find('sourceCurrency').text
             product_availability_local = prod.find('product_availability_local').text
             product_availability = prod.find('product_availability').text
             antey_collection.find_one_and_update({'product_sku': product_sku},
                                                  {'$set': {'product_status': product_status,
                                                            'product_price': product_price,
                                                            'product_currency': product_currency,
                                                            'product_price_online': product_price_online,
                                                            'product_price_currency_online': product_price_currency_online,
                                                            'sourcePrice': sourcePrice,
                                                            'sourceCurrency': sourceCurrency,
                                                            'product_availability_local': product_availability_local,
                                                            'product_availability': product_availability}})


     def antey_brands_update(db, antey_link, antey_brands_update_list):
         antey_collection = db['antey_db']
         antey_site = Scraper.get_soup(antey_link)
         products = antey_site.find_all('product')
         for prod in products:
            manufacturer_name = prod.find('manufacturer_name').text
            if manufacturer_name in antey_brands_update_list:
                         product_sku = prod.find('product_sku').text
                         product_categoryId = prod.find('product_categoryId').text
                         product_name = prod.find('product_name').text
                         product_model = prod.find('product_model').text
                         product_seria = prod.find('product_seria').text
                         product_status = prod.find('product_status').text
                         product_price = prod.find('product_price').text
                         product_currency = prod.find('product_currency').text
                         product_price_online = prod.find('product_price_online').text
                         product_price_currency_online = prod.find('product_price_currency_online').text
                         sourcePrice = prod.find('sourcePrice').text
                         sourceCurrency = prod.find('sourceCurrency').text
                         product_availability_local = prod.find('product_availability_local').text
                         product_availability = prod.find('product_availability').text
                         antey_dataset = {
                             'product_sku': product_sku,
                             'product_categoryId': product_categoryId,
                             'product_name': product_name,
                             'product_model': product_model,
                             'product_seria': product_seria,
                             'product_status': product_status,
                             'product_price': product_price,
                             'product_currency': product_currency,
                             'product_price_online': product_price_online,
                             'product_price_currency_online': product_price_currency_online,
                             'sourcePrice': sourcePrice,
                             'sourceCurrency': sourceCurrency,
                             'product_availability_local': product_availability_local,
                             'product_availability': product_availability,
                         }

                         if prod.find('ext_info').text == 'true':
                             description = prod.find('description')
                             try:
                                 description = description.text
                             except:
                                 description = ' '
                         else:
                             description = ' '

                         antey_dataset['description'] = description
                         param_values = prod.find_all('parameter')
                         for param in param_values:
                             param_category = (str(param).split('\"')[1]).replace('.', '')
                             param = param.text
                             antey_dataset[param_category] = param

                         update = antey_collection.find_one_and_update({'product_sku': product_sku},
                                                              {'$set': antey_dataset})
                         if update == None:
                             antey_dataset['manufacturer_name'] = manufacturer_name
                             antey_collection.insert_one(antey_dataset)
