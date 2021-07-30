from celery import Celery
from time import sleep
import os

BROKER_URL = 'mongodb://localhost:27017/jobs'
app = Celery('tasks', broker=BROKER_URL)
app.conf.update(CELERY_TIMEZONE = 'Asia/Ho_Chi_Minh')
app.config_from_object('celeryconfig')

@app.task
def add(x, y):
    return x + y

@app.task
def sub(x, y):
	return x - y

@app.task
def daily_crawl():
    os.chdir("..\wunderground")
    os.system("scrapy crawl monthly -a key=\"Quận Tân Bình\" -a period=\"2021-6 2021-7\" -o items.json")
    # subprocess.call(['scrapy','crawl','monthly','-a','/home/metabase/metabase.jar'])