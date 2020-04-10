from celery import Celery
import os
from scraper.scraper_2 import agromat_scraper
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pandas as pd
import requests as req

app = Celery("fr_scrapper")

@app.task
def agromat_scraper(agromat_link):
    with urlopen(agromat_link) as r:
        soup = BeautifulSoup(r.read().decode('utf-8'), 'xml')
        agromat_dataset_list = list()
        for prod in soup.find_all('product'):
            agromat_dataset = {
                'Articul': prod.find('Articul').text,
                'Available': prod.find('Available').text,
                'Brand': prod.find('Brand').text,
                'Category': prod.find('Category').text,
                'Code': prod.find('Code').text,
                'Collections': prod.find('Collections').text,
                'Country': prod.find('Country').text,
                'Group': prod.find('Group').text,
                'Height': prod.find('Height').text,
                'Images': prod.find('Images').text,
                'Length': prod.find('Length').text,
                'KgInPackage': prod.find('Length').text,
                'Measure': prod.find('Measure').text,
                'MetersInPackage': prod.find('MetersInPackage').text,
                'Name': prod.find('Name').text,
                'PackagesInPallets': prod.find('PackagesInPallets').text,
                'PiecesInPackage': prod.find('PiecesInPackage').text,
                'RrcPrice': prod.find('RrcPrice').text,
                'Sort': prod.find('Sort').text,
                'Status': prod.find('Status').text,
                'Width': prod.find('Width').text
            }
            agromat_dataset_list.append(agromat_dataset)

        return agromat_dataset_list

@app.task
def get_soup(link):
    resp = req.get(link)
    soup = BeautifulSoup(resp.text, 'xml')
    return soup

@app.task
def get_param_list(get_soup, parameter):
    param_list = get_soup.find_all(parameter)
    param_list1 = list()
    for x in param_list:
        x = str(x).split('\"')[1]
        param_list1.append(x)

    param_list = list(set(param_list1))
    return param_list

@app.task
def get_category_list(get_soup):
    category_list = get_soup.find_all('category')
    category_list1 = list()
    for x in category_list:
        x = x.text
        category_list1.append(x)
    category_list = category_list1
    return category_list

@app.task
def get_sandi_produts(get_soup):
    products = get_soup.find_all('offer')
    sandi_dataset_list = list()
    for prod in products:
        main_list = (str(prod).split('>')[0]).split('\"')
        sandi_dataset = {
            'id': main_list[3],
            'name': prod.find('name').text,
            'aviable': main_list[1],
            'instock': main_list[5],
            'price': prod.find('price').text,
            'currencyId': prod.find('currencyId').text,
            'delivery': prod.find('delivery').text,
            'vendor': prod.find('vendor').text,
            'vendorCode': prod.find('vendorCode').text,
            'model': prod.find('model').text,
            'description': prod.find('description').text,
            'categoryId': prod.find('categoryId').text,
        }
        if prod.find('param') != None:
            prod_param = prod.find_all('param')
            for param in prod_param:
                param_category = (str(param).split('\"')[1]).replace('.', '')
                sandi_dataset[param_category] = param.text

        sandi_dataset_list.append(sandi_dataset)
    return sandi_dataset_list

@app.task
def get_antey_products(get_soup):
    products = get_soup.find_all('product')
    antey_dataset_list = list()
    for prod in products:
        antey_dataset = {
            'product_sku': prod.find('product_sku').text,
            'product_categoryId': prod.find('product_categoryId').text,
            'product_name': prod.find('product_name').text,
            'product_model': prod.find('product_model').text,
            'manufacturer_name': prod.find('manufacturer_name').text,
            'product_seria': prod.find('product_seria').text,
            'product_status': prod.find('product_status').text,
            'product_price': prod.find('product_price').text,
            'product_currency': prod.find('product_currency').text,
            'product_price_online': prod.find('product_price_online').text,
            'product_price_currency_online': prod.find('product_price_currency_online').text,
            'sourcePrice': prod.find('sourcePrice').text,
            'sourceCurrency': prod.find('sourceCurrency').text,
            'product_availability_local': prod.find('product_availability_local').text,
            'product_availability': prod.find('product_availability').text,
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

        antey_dataset_list.append(antey_dataset)
    return antey_dataset_list

@app.task
def get_sandi_brands(get_soup):

    products = get_soup.find_all('offer')
    sandi_brands_list = list()
    for prod in products:
        if prod.find('param') != None:
            prod_param = prod.find_all('param')
            for param in prod_param:
                param_category = (str(param).split('\"')[1]).replace('.', '')
                if param_category == 'Бренд':
                    param = param.text
                    sandi_brands_list.append(param)

    sandi_brands_list = list(set(sandi_brands_list))
    sandi_brands_list.sort()
    return sandi_brands_list

@app.task
def get_antey_brands(get_soup):

    products = get_soup.find_all('product')
    antey_brands_list = list()
    for prod in products:
        manufacturer_name = prod.find('manufacturer_name').text
        antey_brands_list.append(manufacturer_name)

    antey_brands_list = list(set(antey_brands_list))
    antey_brands_list.remove('')
    antey_brands_list.sort()
    return antey_brands_list

@app.task
def connection(table_name):
    client = MongoClient('mongodb://romasoya1402:Roma1989Soya@cluster0-shard-00-00-zkewx.mongodb.net:27017,cluster0-shard-00-01-zkewx.mongodb.net:27017,cluster0-shard-00-02-zkewx.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client.b2b
    table = db[table_name].find()

    return table

@app.task
def prepare_csv(table_name):
    docs = pd.DataFrame(list(connection(table_name)))
    string = 'app/db/data/' + str(table_name) + '.csv'
    docs.to_csv(string, index=False)

@app.task
def sandi_update_all(db, site):
    sandi_collection = db['sandi_db']
    sandi_collection.delete_many({})
    sandi_dataset_list = get_sandi_produts(get_soup(site))
    sandi_collection.insert_many(sandi_dataset_list)



@app.task
def sandi_brands_update(db, sandi_link, sandi_brands_update_list):
    sandi_collection = db['sandi_db']
    sandi_site = get_soup(sandi_link)
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
                        aviable = main_list[1]
                        sandi_dataset = {
                            'id': main_list[3],
                            'name': prod.find('name').text,
                            'aviable': aviable,
                            'instock': main_list[5],
                            'price': prod.find('price').text,
                            'currencyId': prod.find('currencyId').text,
                            'delivery': prod.find('delivery').text,
                            'vendor': prod.find('vendor').text,
                            'vendorCode': prod.find('vendorCode').text,
                            'model': prod.find('model').text,
                            'description': prod.find('description').text,
                            'categoryId': prod.find('categoryId').text,
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
     antey_dataset_list = get_antey_products(get_soup(antey_link))
     antey_collection.insert_many(antey_dataset_list)



@app.task
def antey_brands_update(db, antey_link, antey_brands_update_list):
 antey_collection = db['antey_db']
 antey_site = get_soup(antey_link)
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
def agromat_brands_update(db, agromat_link, antey_brands_update_list):
 agromat_collection = db['agromat_db']
 with urlopen(agromat_link) as r:
     xml = r.read().decode('utf-8')
     soup = BeautifulSoup(xml, 'xml')
     for prod in soup.find_all('product'):
         Brand = prod.find('Brand').text
         if Brand in antey_brands_update_list:
             agromat_dataset = {
                 'Articul': prod.find('Articul').text,
                 'Available': prod.find('Available').text,
                 'Category': prod.find('Category').text,
                 'Code': prod.find('Code').text,
                 'Collections': prod.find('Collections').text,
                 'Country': prod.find('Country').text,
                 'Group': prod.find('Group').text,
                 'Height': prod.find('Height').text,
                 'Images': prod.find('Images').text,
                 'Length': prod.find('Length').text,
                 'KgInPackage': prod.find('Length').text,
                 'Measure': prod.find('Measure').text,
                 'MetersInPackage': prod.find('MetersInPackage').text,
                 'Name': prod.find('Name').text,
                 'PackagesInPallets': prod.find('PackagesInPallets').text,
                 'PiecesInPackage': prod.find('PiecesInPackage').text,
                 'RrcPrice': prod.find('RrcPrice').text,
                 'Sort': prod.find('Sort').text,
                 'Status': prod.find('Status').text,
                 'Width': prod.find('Width').text
             }
             update = agromat_collection.find_one_and_update({'Code': prod.find('Code').text},
                                                           {'$set': agromat_dataset})
             if update == None:
                 agromat_dataset['Brand'] = Brand
                 agromat_collection.insert_one(agromat_dataset)



app.conf.update(BROKER_URL=os.environ['REDIS_URL'],CELERY_RESULT_BACKEND = os.environ['REDIS_URL'])
