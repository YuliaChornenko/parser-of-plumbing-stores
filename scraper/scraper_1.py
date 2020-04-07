from bs4 import BeautifulSoup
import requests as req
import lxml


# resp = req.get('https://b2b-sandi.com.ua/export_xml/2b4b03e329fa14abe9c4c89fe5b591cd')
# soup = BeautifulSoup(resp.text, 'xml')
# param_list = soup.find_all('param')
#
# param_list1 = list()
# for x in param_list:
#     x = str(x).split('\"')[1]
#     param_list1.append(x)
#
# param_list = list(set(param_list1))
#
# category_list = soup.find_all('category')
# category_list1 = list()
# for x in category_list:
#     x = x.text
#     category_list1.append(x)
# category_list = category_list1
#
# products = soup.find_all('offer')
#
# for prod in products:
#     main_list = (str(prod).split('>')[0]).split('\"')
#     id = main_list[3]
#     aviable = main_list[1]
#     instock = main_list[5]
#     name = prod.find('name').text
#     delivery = prod.find('delivery').text
#     vendor = prod.find('vendor').text
#     vendorCode = prod.find('vendorCode').text
#     model = prod.find('model').text
#     description = prod.find('description').text
#     price = prod.find('price').text
#     currencyId = prod.find('currencyId').text
#     categoryId = prod.find('categoryId').text
#     if prod.find('param') != None:
#         prod_param = prod.find_all('param')
#         for param in prod_param:
#             param_category = str(param).split('\"')[1]
#             param = param.text

class Scraper:

    def get_soup(link):
        resp = req.get(link)
        soup = BeautifulSoup(resp.text, 'xml')
        return soup

    def get_param_list(get_soup, parameter):
        param_list = get_soup.find_all(parameter)
        param_list1 = list()
        for x in param_list:
            x = str(x).split('\"')[1]
            param_list1.append(x)

        param_list = list(set(param_list1))
        return param_list

    def get_category_list(get_soup):
        category_list = get_soup.find_all('category')
        category_list1 = list()
        for x in category_list:
            x = x.text
            category_list1.append(x)
        category_list = category_list1
        return category_list

    def get_sandi_produts(get_soup):
        products = get_soup.find_all('offer')
        for prod in products:
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
            if prod.find('param') != None:
                prod_param = prod.find_all('param')
                for param in prod_param:
                    param_category = str(param).split('\"')[1]
                    param = param.text

    def get_antey_products(get_soup):
        products = get_soup.find_all('product')
        for prod in products:
            product_sku = prod.find('product_sku').text
            product_categoryId = prod.find('product_categoryId').text
            product_name = prod.find('product_name').text
            product_model = prod.find('product_model').text
            manufacturer_name = prod.find('manufacturer_name').text
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
            if prod.find('ext_info').text == 'true':
                description = prod.find('description')
                try:
                    description = description.text
                except:
                    description = ' '
            else:
                description = ' '
            param_values = prod.find_all('parameter')
            for param in param_values:
                param_category = str(param).split('\"')[1]
                param = param.text
