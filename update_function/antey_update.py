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