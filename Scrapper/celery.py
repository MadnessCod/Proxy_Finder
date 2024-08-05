from celery import Celery
from celery.schedules import crontab

from local_settings import BROKER_URL, BACKEND_URL


print(BROKER_URL, BACKEND_URL)
app = Celery('ProxyFinder', broker=BROKER_URL, backend=BACKEND_URL)

app.autodiscover_tasks(['Scrapper'])

app.conf.broker_connection_retry = True

app.conf.beat_schedule = {
    "scraping": {
        "task": "Scrapper.tasks.main",
        "schedule": crontab('*/10'),
    },
    "evaluator": {
        "task": "Scrapper.tasks.proxy_evaluator_main",
        "schedule": crontab('*/5'),
    },
}
