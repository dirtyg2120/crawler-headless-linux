# Report week 3 (not completed)

This is a report during my intern course.



## 1. Tasks:

Improve crawler system.
Focus on:

- Scheduling
- Running on a headless server
- Building an automated pipeline
- Design your system on draw.io
- Bypass security

## 2. My works:

### Building an automated pipeline

Thanks to anh Đức's and anh Phúc's comments :))) on my works last time, I have improved a little bit on my crawler system.

First is fix the hard code which you guys told me. Second is I made my system become more automatic. Instead of changing the source code to crawl on 1 or multiple page and multiple point of time, I can now do all of that with one command line. Here is how I do it.

Because the url of each place is hard to generate, so I used **Selenium** to automatically search for a place and navigate to the first option in drop down menu.

<img src=".\report\img\keysearch.png" alt="image-20210614165332989" style="zoom: 67%;" />

Then I took the url of place and used it to generate many other pages on that place. For example, after click on the first option from previous part. I got this

```python
place = 'quận-tân-bình'
```



Another thing I want to get is the period of history weather data. So I adjusted `__init__()` function of spider to take my extra arguments, which is `key` to search for place and `period` to get start and end time crawl on demand.

```python
def __init__(self, key=None, period=None,*args, **kwargs):
    super(WundergroundSpider, self).__init__(*args, **kwargs)
    self.key = key
    self.start = period.split(' ')[0]
    self.end = period.split(' ')[1]
    PATH = "..\chromedriver.exe"
    self.driver = webdriver.Chrome(PATH)
```

For example, if I run a command with `key='Quận Tân Bình' period='2020-11 2021-2'`, I will get all the recorded data in 4 month **11/2020**, **12/2020**, **1/2021**, **2/2021** at **Quận Tân Bình**. And I generated all the urls with:

```python
def get_url_list(place, start, end):
    url_lst = []
    datelist = get_datelist(start, end)
    for date in datelist:
        new_url = f'https://www.wunderground.com/history/monthly/vn/{place}/VVTS/date/{date}'
        url_lst.append(new_url)
    
    return url_lst
```

`get_datelist()`is just a function I used to generate a list of date from the given `period`.



Finally, to get data from a place in a period of time, I used the command below:

```shell
$ scrapy crawl monthly -a key=<place-to-search> -a period=<crawl-period>
```

For example:

```shell
$ scrapy crawl monthly -a key='Quận Tân Bình' -a period='2020-11 2021-2' -o items.json
```

And I got this as result:

<img src=".\report\img\mongo_week3.png" alt="image-20210614165332989" style="zoom: 67%;" />



**But there is a drawback of my solution:**

* The argument `key` from command line need to be very similar to where you want to get the data. For example, If you search for ***Quận Tân Bình***, but in command the argument is only `-a key='Tân Bình`, result will be wrong.

<img src=".\report\img\wrong_week3.png" alt="image-20210614165332989" style="zoom:80%;" />

### Scheduling task

Last week, I just scheduled the task with a period of time like '*crawl every 5 minutes*'. The disadvantage of period is that if I want to run task at **9-PM**/**21 o'clock** on company server, I can not always wait until 9-PM and set it to run '*crawl every 1 days*'. It's possible but not good. A solution for this issue is using **crontab** package, which is made similar to **cron** command in **Unix-like OS**.

First, I had to enable UTC and set timezone:

```python
enable_utc = True
CELERY_TIMEZONE = "Asia/Ho_Chi_Minh"
```

Then I change value in `schedule` key with **crontab**:

```python
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'crawl': {
        'task': 'tasks.daily_crawl',
        'schedule': crontab(minute='0', hour='8', day_of_week='*/2', day_of_month='*', month_of_year='*'),
    },
}
```

All the change is in [celeryconfig.py](.\my_celery\celeryconfig.py) file

And with the code above, I will have my system run at **8:00 AM, every 2 days of the week**