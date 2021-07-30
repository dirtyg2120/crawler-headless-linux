# simple-web-crawler

#### Week 2 report



## 1. Tasks:

Build a simple web crawler to crawl the link below and store results in MongoDB, and using Celery to schedule task.

Link: *[https://www.wunderground.com/history/daily/vn/qu%E1%BA%ADn-9/VVTS](https://www.wunderground.com/history/daily/vn/quận-9/VVTS)*

<img src=".\img\wunder_daily.png" alt="image-20210614165332989" style="zoom: 67%;" />

 ## 2. Solution:

The idea here is I set the job of crawling this page as a task, and run it on schedule, maybe once a day with **Celery** and update new data to **MongoDB**.

But at that time, I thought learning about **Celery** for this idea would cost a lot of time and I also want to try crawling multiple page with the same contents, so I choose the monthly history page to crawl, instead. And here is the link: *https://www.wunderground.com/history/monthly/vn/qu%E1%BA%ADn-t%C3%A2n-b%C3%ACnh/VVTS/date/2021-6*

<img src=".\img\wunder_monly.png" alt="image-20210614165332989" style="zoom: 67%;" />

My implementation for this page data structure is:

```python
class WundergroundItem(scrapy.Item):
    date = Field() # Time

    temp_max = Field() # Temperature (°C)
    temp_min = Field()
    temp_avg = Field()

    dewpoint_max = Field() # Dew Point (°C)
    dewpoint_min = Field()
    dewpoint_avg = Field()

    humidity_max = Field() # Humidity (%)
    humidity_min = Field()
    humidity_avg = Field()

    windspeed_max = Field() # Wind Speed (mph)
    windspeed_min = Field()
    windspeed_avg = Field()

    pressure_max = Field() # Pressure (Hg)
    pressure_min = Field()
    pressure_avg = Field()

    precipitation = Field() # Precipitation (in)
```

The difficulty about this page rather than two previous I have done is that it render *dynamic* page. The data is hidden behind JavaScript, which means I have to interact with the page or wait for an amount of time to see the data I need.

And in this page, there are two things prevent me from getting what I need:

1. Changing temperature format (from °F to °C) button.
2. Data table need about 5 seconds to load.

<img src=".\img\wunder_firstload.png" alt="image-20210614165332989" style="zoom: 67%;" />

<center><i>Before data loaded</i></center>

So I have to find a helper tool to solve this, because as I found One major setback of **Scrapy** is that it does not render JavaScript; you have to send Ajax requests to get data hidden behind JavaScript. And **Selenium** was the answer for me. 

**Selenium** is a Web Browser Automation Tool originally designed to automate web applications for testing purposes. The major advantage Selenium is that it can re-renders a given link with browser driver and loads JavaScript to access data behind JavaScript without sending additional requests. But I also like the structure of **Scrapy** framework, so I combined these two.



The required package import for **Selenium**:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
```

For rendering webpage, I used ChromeDriver:

```python
def __init__(self, *args, **kwargs):
    super(WundergroundSpider, self).__init__(*args, **kwargs)
    PATH = "..\chromedriver.exe"
    self.driver = webdriver.Chrome(PATH)     
```

With the help of **Selenium** I can solve the problems above with this code line:

```python
self.driver.implicitly_wait(5)
```

This line will make the rendered page waits at max 5 second before an element was found on demand. And I use this to wait for the data table appears.

With the *"changing temperature format button"* problem, I can automate the way I press the button as below:

```python
setting = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@id="wuSettings"]/i')))
setting.click()
celsius = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="wuSettings-quick"]/div/a[2]')))
celsius.click()
```



In the data structure, there are some features have 3 values (max, min, average). In this report, I will show how I parse average value only, for the full implementation you can view this file [wunderground_spider.py](./wunderground/spiders/wunderground_spider.py).

```python
self.driver.get(response.url)
length = len(self.driver.find_elements_by_xpath('//table[@class="days ng-star-inserted"]/tbody/tr/td[2]/table/tr'))
information = self.driver.find_element_by_xpath('//table[@class="days ng-star-inserted"]/tbody/tr')
myitems = []

for i in range(2, length+1):
	history = items.WundergroundItem()
    history['date'] = self.getDate(response, i, information)
    history['temp_avg'] = information.find_element_by_xpath('.//td[2]/table/tr[{}]/td[2]'.format(str(i))).text
    history['dewpoint_avg'] = information.find_element_by_xpath('.//td[3]/table/tr[{}]/td[2]'.format(str(i))).text
    history['humidity_avg'] = information.find_element_by_xpath('.//td[4]/table/tr[{}]/td[2]'.format(str(i))).text
    history['windspeed_avg'] = information.find_element_by_xpath('.//td[5]/table/tr[{}]/td[2]'.format(str(i))).text
    history['pressure_avg'] = information.find_element_by_xpath('.//td[6]/table/tr[{}]/td[2]'.format(str(i))).text
    history['precipitation'] = information.find_element_by_xpath('.//td[7]/table/tr[{}]/td'.format(str(i))).text

    myitems.append(history)
    
self.driver.close()
return myitems
```

The `getDate()` function is used to get the day, month and year then concatenate it into 1 string.

```python
def getDate(self, response, i, information):
    day = information.find_element_by_xpath('.//td[1]/table/tr[{}]/td'.format(str(i))).text
    month = response.request.url.split('-')[-1]
    year = response.request.url.split('/')[-1][:4]
    return day + '-' + month + '-' + year
```



That's all for the page 1 page crawler. Now for the multiple crawl, I added a list of urls I want to crawl first:

```python
other_urls = [
    "https://www.wunderground.com/history/monthly/vn/qu%E1%BA%ADn-t%C3%A2n-b%C3%ACnh/VVTS/date/2021-3",
    "https://www.wunderground.com/history/monthly/vn/qu%E1%BA%ADn-t%C3%A2n-b%C3%ACnh/VVTS/date/2021-4",
]
```

And after the `for` loop in `parse()` function, I removed the urls if it was crawled else keep crawling.

```python
self.other_urls.remove(response.url)
if self.other_urls:
    res = Request(self.other_urls[0], self.parse)
    myitems.append(res)
```

With the following command, I will get all the data I need in March and April of 2021:

```shell
$ scrapy crawl wunderground_spider -o items.json
```

<img src=".\img\wunder_result.png" alt="image-20210614165332989" style="zoom: 67%;" />



## 3. Schedule task with Celery:

After researching more about **Celery**, I found that there are 3 main features of **Celery** which can be used in a web crawler:

1. **Scheduling** - I can specify the time when to run a task in seconds/datetime, or provide simple interval or crontab expressions for periodic tasks.
2. **Time & Rate Limits** - Number of tasks executed per second/minute/hour, as well as task processing duration can be controlled and/or be set as a default.
3. **High availability** and **horizontal scaling** - Celery system has multiple broker and multiple workers support, it can run on a single machine, on multiple machines, or even across data centers.

But at this time, I have only known how to schedule a task. First, I assigned task in [tasks.py](.\my_celery\tasks.py) file. **Celery** will need a broker but because I still confuse about Message Broker, so I use **MongoDB** as temporary one. 

For the task, I assigned to a function which will run **Scrapy** command in shell.

```python
from celery import Celery
import os

BROKER_URL = 'mongodb://localhost:27017/jobs'
app = Celery('tasks', broker=BROKER_URL)
app.config_from_object('celeryconfig')

@app.task
def daily_crawl():
    os.chdir("D:\ARI\simple-web-crawler\wunderground")        
    os.system("scrapy crawl wunderground_spider -o itemss.json")
```

Final step is configuring **Celery**, [celeryconfig.py](.\my_celery\celeryconfig.py) with:

* `CELERY_RESULT_BACKEND` and `CELERY_MONGODB_BACKEND_SETTINGS` are used to connect to my local **MongDB** database.
* `CELERYBEAT_SCHEDULE` is used to set schedule for the assigned task.

```python
from datetime import timedelta

CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": "127.0.0.1",
    "port": 27017,
    "database": "jobs", 
    "taskmeta_collection": "stock_taskmeta_collection",
}

CELERYBEAT_SCHEDULE = {
    'crawl': {
        'task': 'tasks.daily_crawl',
        'schedule': timedelta(minutes=1),
    },
}
```

To run the task, I need to open 2 terminal and run with each of the commands below:

```shell
$ celery -A tasks worker --loglevel=info
```

```shell
$ celery -A tasks beat
```



* Giữ page, ko tắt