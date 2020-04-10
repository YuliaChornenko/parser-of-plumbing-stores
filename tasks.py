from celery import Celery
import os
from scraper.scraper_1 import Scraper

app = Celery("fr_scrapper_scheduller")

@app.task
def add(db, site):
    sandi_collection = db['sandi_db']
    sandi_collection.delete_many({})
    sandi_dataset_list = Scraper.get_sandi_produts(Scraper.get_soup(site))
    sandi_collection.insert_many(sandi_dataset_list)

app.conf.update(BROKER_URL=os.environ['REDIS_URL'],CELERY_RESULT_BACKEND = os.environ['REDIS_URL'])
