from celery.schedules import crontab
from datetime import timedelta

CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": "127.0.0.1",
    "port": 27017,
    "database": "jobs", 
    "taskmeta_collection": "stock_taskmeta_collection",
}

enable_utc = True
CELERY_TIMEZONE = "Asia/Ho_Chi_Minh"


CELERYBEAT_SCHEDULE = {
    # 'add': {
    #     'task': 'tasks.add',
    #     # 'schedule': crontab(minute='*/1'),
    #     'schedule': timedelta(seconds=20),
    #     'args': (11,22),
    # },
    # 'sub': {
    #     'task': 'tasks.sub',
    #     'schedule': crontab(minute='56', hour='20', day_of_week='0', day_of_month='*', month_of_year='*'),
    #     'args': (11,22),
    # },
    'crawl': {
        'task': 'tasks.daily_crawl',
        # 'schedule': crontab(minute='0', hour='8', day_of_week='*/2', day_of_month='*', month_of_year='*'),
        'schedule': crontab(minute='*/2', hour='*', day_of_week='*', day_of_month='*', month_of_year='*'),
    },
}