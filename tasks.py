from celery import Celery
import os

app = Celery("fr_scrapper_scheduller")

@app.task
def add(db, site):
    print('TASK STARTER')
    sandi_collection = db['sandi_db']
    print(222222222222222222222222222222)
    sandi_collection.delete_many({})
    print(333333333333333333333333333333)

app.conf.update(BROKER_URL=os.environ['REDIS_URL'],CELERY_RESULT_BACKEND = os.environ['REDIS_URL'])
