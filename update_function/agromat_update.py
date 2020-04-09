from scraper.scraper_2 import agromat_scraper

class AgromatUpdate:

     def agromat_update_all(db, agromat_link):
         agromat_collection = db['agromat_db']
         agromat_collection.delete_many({})
         agromat_dataset_list = agromat_scraper(agromat_link)
         agromat_collection.insert_many(agromat_dataset_list)
