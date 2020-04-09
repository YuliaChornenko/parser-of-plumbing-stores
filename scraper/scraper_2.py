from urllib.request import urlopen
from bs4 import BeautifulSoup


def agromat_scraper(agromat_link):
    with urlopen(agromat_link) as r:
        xml = r.read().decode('utf-8')
        soup = BeautifulSoup(xml, 'xml')
        products = soup.find_all('product')
        agromat_dataset_list = list()
        for prod in products:
            Articul = prod.find('Articul').text
            Available = prod.find('Available').text
            Brand = prod.find('Brand').text
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
                'Brand': Brand,
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

            agromat_dataset_list.append(agromat_dataset)

        return agromat_dataset_list
