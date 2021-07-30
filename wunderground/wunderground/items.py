# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class WundergroundItem(scrapy.Item):
    date = Field() # Time
    
    temp_max = Field() # Temperature (° C)
    temp_min = Field()
    temp_avg = Field()
    
    dewpoint_max = Field() # Dew Point (° C)
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