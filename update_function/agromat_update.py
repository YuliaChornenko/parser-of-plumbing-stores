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
