from scrapy import Spider, Request
from scrapy.selector import Selector

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

from wunderground import items
import time


class WundergroundSpider(Spider):
    name = 'monthly'
    allowed_domains = ['wunderground.com']
    start_urls = ['https://www.wunderground.com/']
    other_urls = []

    def __init__(self, key=None, period=None,*args, **kwargs):
        super(WundergroundSpider, self).__init__(*args, **kwargs)
        self.key = key
        self.start = period.split(' ')[0]
        self.end = period.split(' ')[1]
        PATH = "../geckodriver"
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        # self.display = Display(visible=False, size=(800, 600))
        # self.display.start()
        self.driver = webdriver.Firefox(executable_path=PATH, options=firefox_options)

    def parse(self, response):
        self.driver.get(response.url)
        
        if str(response.url) == 'https://www.wunderground.com/':
            place = self.automate(self.key)
            self.other_urls += get_url_list(place, self.start, self.end)
            self.driver.get(self.other_urls[0])
        time.sleep(5)

        length = len(self.driver.find_elements_by_xpath('//table[@class="days ng-star-inserted"]/tbody/tr/td[2]/table/tr'))
        information = self.driver.find_element_by_xpath('//table[@class="days ng-star-inserted"]/tbody/tr')
        myitems = []

        for i in range(2, length+1):
            history = items.WundergroundItem()
            history['date'] = self.getDate(self.driver.current_url, i, information)

            history['temp_max'] = information.find_element_by_xpath('.//td[2]/table/tr[{}]/td[1]'.format(str(i))).text
            history['temp_avg'] = information.find_element_by_xpath('.//td[2]/table/tr[{}]/td[2]'.format(str(i))).text
            history['temp_min'] = information.find_element_by_xpath('.//td[2]/table/tr[{}]/td[3]'.format(str(i))).text
            
            history['dewpoint_max'] = information.find_element_by_xpath('.//td[3]/table/tr[{}]/td[1]'.format(str(i))).text
            history['dewpoint_avg'] = information.find_element_by_xpath('.//td[3]/table/tr[{}]/td[2]'.format(str(i))).text
            history['dewpoint_min'] = information.find_element_by_xpath('.//td[3]/table/tr[{}]/td[3]'.format(str(i))).text

            history['humidity_max'] = information.find_element_by_xpath('.//td[4]/table/tr[{}]/td[1]'.format(str(i))).text
            history['humidity_avg'] = information.find_element_by_xpath('.//td[4]/table/tr[{}]/td[2]'.format(str(i))).text
            history['humidity_min'] = information.find_element_by_xpath('.//td[4]/table/tr[{}]/td[3]'.format(str(i))).text

            history['windspeed_max'] = information.find_element_by_xpath('.//td[5]/table/tr[{}]/td[1]'.format(str(i))).text
            history['windspeed_avg'] = information.find_element_by_xpath('.//td[5]/table/tr[{}]/td[2]'.format(str(i))).text
            history['windspeed_min'] = information.find_element_by_xpath('.//td[5]/table/tr[{}]/td[3]'.format(str(i))).text

            history['pressure_max'] = information.find_element_by_xpath('.//td[6]/table/tr[{}]/td[1]'.format(str(i))).text
            history['pressure_avg'] = information.find_element_by_xpath('.//td[6]/table/tr[{}]/td[2]'.format(str(i))).text
            history['pressure_min'] = information.find_element_by_xpath('.//td[6]/table/tr[{}]/td[3]'.format(str(i))).text

            history['precipitation'] = information.find_element_by_xpath('.//td[7]/table/tr[{}]/td'.format(str(i))).text

            myitems.append(history)
        
        self.other_urls.remove(self.other_urls[0])
        if self.other_urls:
            res = Request(self.other_urls[0], self.parse)
            myitems.append(res)
        else:
            self.driver.close()
        return myitems


    def getDate(self, url, i, information):
        day = information.find_element_by_xpath('.//td[1]/table/tr[{}]/td'.format(str(i))).text
        month = url.split('-')[-1]
        year = url.split('/')[-1][:4]
        return day + '-' + month + '-' + year

    def automate(self, key):
        wait = WebDriverWait(self.driver, 10)
        time.sleep(5)
        search = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="wuSearch"]')))
        search.click()
        search.send_keys(key)
        
        option = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="needsclick needsfocus"][1]')))
        option.click()
        
        place = self.driver.current_url.split('/')[-1]

        # wait.until(EC.presence_of_element_located((By.XPATH, '//table[@class="days ng-star-inserted"]/tbody/tr')))
        return place
        # time.sleep(5)
        # setting = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@id="wuSettings"]/i')))
        # setting.click()
        # celsius = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="wuSettings-quick"]/div/a[2]')))
        # celsius.click()

def get_datelist(start, end):
    lst = []
    start_year = int(start[:4])
    end_year = int(end[:4])
    start_month = int(start.split('-')[1])
    end_month = int(end.split('-')[1])

    if start == end:
	    lst.append(start)
    elif start_year == end_year:
        for month in range(start_month, end_month+1):
            lst.append(str(start_year) + '-' + str(month))
    else:
        for year in range(start_year, end_year+1):
            if year == start_year:
                lst += [str(year) + '-' + str(month) for month in range(start_month, 13)]
            elif year == end_year:
                lst += [str(year) + '-' + str(month) for month in range(1, end_month+1)]
            else:
                lst += [str(year) + '-' + str(month) for month in range(1, 13)]
    
    return lst

def get_url_list(place, start, end):
    url_lst = []
    datelist = get_datelist(start, end)
    for date in datelist:
        new_url = f'https://www.wunderground.com/history/monthly/vn/{place}/VVTS/date/{date}'
        url_lst.append(new_url)
    
    return url_lst