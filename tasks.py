from celery import Celery
import os

app = Celery("fr_scrapper_scheduller")

@app.task
def add(x, y):
    print('TASK STARTER')
    return x + y

app.conf.update(BROKER_URL=os.environ['REDIS_URL'],CELERY_RESULT_BACKEND = os.environ['REDIS_URL'])
