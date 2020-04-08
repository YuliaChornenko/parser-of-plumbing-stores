from scraper.scraper_1 import Scraper

class SandiUpdate(Scraper):

     def sandi_update_all(db, sandi_link):
         sandi_collection = db['sandi_db']
         sandi_collection.delete_many({})
         sandi_dataset_list = Scraper.get_sandi_produts(Scraper.get_soup(sandi_link))
         sandi_collection.insert_many(sandi_dataset_list)

