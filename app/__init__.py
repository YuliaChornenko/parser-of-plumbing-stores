from flask import Flask
from celery import Celery
import os

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['celery_result_backend'],
        broker=app.config['celery_broker_url']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.update(
    celery_broker_url=os.environ.get("REDIS_URL"),
    celery_result_backend=os.environ.get("REDIS_URL")
)
app.config.update(
    task_serializer='pickle',
    accept_content=['pickle', 'json'],  # Ignore other content
    result_serializer='pickle',
    timezone='Europe/Oslo',
    enable_utc=True,
)



from app import routes