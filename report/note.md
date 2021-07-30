bypass: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

### Target: https://www.wunderground.com/history/monthly/vn/qu%E1%BA%ADn-t%C3%A2n-b%C3%ACnh/VVTS/date/2021-5



# NoSQL

### Why using?

NoSQL bỏ qua tính toàn vẹn của dữ liệu và transacsion để đổi lấy **hiệu suất nhanh và khả năng mở rộng (scalability)**.

### Document Database

Data is stored as BSON/JSON/XML. 

* **MongoDB**
  * Use query document.



# Celery

* Example use case: *https://nickjanetakis.com/blog/4-use-cases-for-when-to-use-celery-in-a-flask-application*
* Running Scrapy in Celery task: *https://codeburst.io/running-scrapy-in-celery-tasks-d81e159921ea*
* Intro: Celery and MongoDB: *https://skillachie.com/2013/06/15/intro-celery-and-mongodb/*
* Main celery feature
  * **Scheduling**. You can specify the time when to run a task in seconds/datetime, or provide simple interval or crontab expressions for periodic tasks.
  * **Monitoring**. Stream of monitoring events is used to provide real-time information about the cluster.
  * **High availability** and **horizontal scaling**. Celery system has multiple broker and multiple workers support, it can run on a single machine, on multiple machines, or even across data centers.
  * **Autoreloading** and **Resource Leak Protection**.
  * **Workflows**. To optimize your work you can create simple and complex workflows using a set of powerful primitives, including grouping, chaining, chunking, etc.
  * **Time & Rate Limits**. Number of tasks executed per second/minute/hour, as well as task processing duration can be controlled and/or be set as a default.
  * **Autoscaling**. Celery dynamically resizes the worker pool depending on load or custom metrics, that is applied to limit memory usage or to enforce a certain service quality.
  * **User Components**. Celery enables fine-grained and tuned control of the worker. User can customize and redefine any worker component.

# Kafka

Viblo: https://viblo.asia/p/kafka-la-gi-gDVK2Q7A5Lj

* Normal system

<img src="C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20210612142630433.png" alt="image-20210612142630433" style="zoom:50%;" />

* Kafka

<img src="C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20210612142658282.png" alt="image-20210612142658282" style="zoom:50%;" />

<img src="C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20210612142709613.png" alt="image-20210612142709613" style="zoom:50%;" />



# Scrapy, Selenium

package: Scrapy, PyMongo, Selenium

* Xpath: `//div[@class="summary"]/h3`  means:

  *Grab all `<h3>` elements that are children of a `<div>` that has a class of `summary`*.

* Use Selenium for dynamic page.
  * Ex: load new thing after click button,...
  * wait() / sleep(): https://selenium-python.readthedocs.io/waits.html
* Use Scrapy for well-organized structured, faster scrape but hard to use for dynamic page.
* Selenium and Scrapy combined: https://stackoverflow.com/questions/17975471/selenium-with-scrapy-for-dynamic-page

*Avoid being blocked: https://webautomation.io/blog/how-to-avoid-getting-blocked-while-web-scraping/*

*Solution for blocking id: https://proxiesapi-com.medium.com/how-to-scrape-weather-data-using-python-scrapy-db02824c1742*

*Source: https://realpython.com/web-scraping-with-scrapy-and-mongodb/*

* test regex: https://regex101.com/
* https://stackoverflow.com/questions/30448532/scrapy-wait-for-a-specific-url-to-be-parsed-before-parsing-others
* scrapy in order: https://stackoverflow.com/questions/6566322/scrapy-crawl-urls-in-order