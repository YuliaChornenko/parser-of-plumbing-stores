from scraper.scraper_1 import Scraper

class AnteyUpdate(Scraper):

     def antey_update_all(db, antey_link):
         antey_collection = db['antey_db']
         antey_collection.delete_many({})
         antey_dataset_list = Scraper.get_antey_products(Scraper.get_soup(antey_link))
         antey_collection.insert_many(antey_dataset_list)