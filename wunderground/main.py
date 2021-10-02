import os

if __name__ == "__main__":
    key = 'Quận Tân Bình'
    period = '2021-7 2021-7'
    output_file = 'items.json'
    # os.system("scrapy crawl monthly -a key='{}' -a period='{}' -o {}".format(key, period, output_file))
    os.system("scrapy crawl monthly -a key='{}' -a period='{}'".format(key, period))