from celery import Celery
import os
from scraper.scraper_1 import Scraper
from scraper.scraper_2 import agromat_scraper
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pandas as pd

app = Celery("fr_scrapper_scheduller")


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

@app.task
def sandi_update_all(db, site):
    sandi_collection = db['sandi_db']
    sandi_collection.delete_many({})
    sandi_dataset_list = Scraper.get_sandi_produts(Scraper.get_soup(site))
    sandi_collection.insert_many(sandi_dataset_list)

@app.task
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

@app.task
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

@app.task
def antey_update_all(db, antey_link):
     antey_collection = db['antey_db']
     antey_collection.delete_many({})
     antey_dataset_list = Scraper.get_antey_products(Scraper.get_soup(antey_link))
     antey_collection.insert_many(antey_dataset_list)

@app.task
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


@app.task
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

@app.task
def agromat_update_all(db, agromat_link):
     agromat_collection = db['agromat_db']
     agromat_collection.delete_many({})
     agromat_dataset_list = agromat_scraper(agromat_link)
     agromat_collection.insert_many(agromat_dataset_list)

@app.task
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

@app.task
def agromat_brands_update(db, agromat_link, antey_brands_update_list):
 agromat_collection = db['agromat_db']
 with urlopen(agromat_link) as r:
     xml = r.read().decode('utf-8')
     soup = BeautifulSoup(xml, 'xml')
     products = soup.find_all('product')
     for prod in products:
         Brand = prod.find('Brand').text
         if Brand in antey_brands_update_list:
             Articul = prod.find('Articul').text
             Available = prod.find('Available').text
             Category = prod.find('Category').text
             Code = prod.find('Code').text
             Collections = prod.find('Collections').text
             Country = prod.find('Country').text
             Group = prod.find('Group').text
             Height = prod.find('Height').text
             Images = prod.find('Images').text
             Length = prod.find('Length').text
             KgInPackage = prod.find('Length').text
             Measure = prod.find('Measure').text
             MetersInPackage = prod.find('MetersInPackage').text
             Name = prod.find('Name').text
             PackagesInPallets = prod.find('PackagesInPallets').text
             PiecesInPackage = prod.find('PiecesInPackage').text
             RrcPrice = prod.find('RrcPrice').text
             Sort = prod.find('Sort').text
             Status = prod.find('Status').text
             Width = prod.find('Width').text
             agromat_dataset = {
                 'Articul': Articul,
                 'Available': Available,
                 'Category': Category,
                 'Code': Code,
                 'Collections': Collections,
                 'Country': Country,
                 'Group': Group,
                 'Height': Height,
                 'Images': Images,
                 'Length': Length,
                 'KgInPackage': KgInPackage,
                 'Measure': Measure,
                 'MetersInPackage': MetersInPackage,
                 'Name': Name,
                 'PackagesInPallets': PackagesInPallets,
                 'PiecesInPackage': PiecesInPackage,
                 'RrcPrice': RrcPrice,
                 'Sort': Sort,
                 'Status': Status,
                 'Width': Width
             }
             update = agromat_collection.find_one_and_update({'Code': Code},
                                                           {'$set': agromat_dataset})
             if update == None:
                 agromat_dataset['Brand'] = Brand
                 agromat_collection.insert_one(agromat_dataset)

app.conf.update(BROKER_URL=os.environ['REDIS_URL'],CELERY_RESULT_BACKEND = os.environ['REDIS_URL'])
