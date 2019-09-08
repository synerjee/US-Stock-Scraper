import scrapy
import csv
from os import path

class StockSpider(scrapy.Spider):
    name='stock'

    def start_requests(self):
        # Entry point of crawling by creating an instance of an object
        # called Request, which is included in Scrapy module

        urls= ['https://finance.yahoo.com/gainers',
               'https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/',
               'http://www.dogsofthedow.com/biggest-stock-gainers-today.htm']

        return [scrapy.Request(url=url, callback=self.parse) for url in urls]


    def parse(self, response):
        url = response.url
        print('Crawling: < {} >'.format(url))

        # Determines the name of CSV file
        mainNames = ['yahoo', 'tradingview', 'dogsofthedow']
        fileName = 'stock.csv'

        # Determines the set of data we should use depending on the website
        default_setup = ('NAME', 'PRICE', 'CHANGE', 'CHANGE RATE')
        yahoo = ('SYMBOL', 'NAME', 'PRICE', 'CHANGE', 'CHANGE RATE', 'VOLUME', 'AVERAGE VOLUME', 'MARKET CAP', 'PE RATIO')
        tradingview = ('SYMBOL', 'LAST PRICE', 'CHANGE RATE', 'CHANGE', 'RATING', 'VOLUME', 'MARKET CAP', 'PE RATIO', 'EPS', 'EMPLOYEES', 'SECTOR')
        dow = ('SYMBOL', 'COMPANY', 'PRICE', 'GAIN RANK', 'DAILY CHANGE', 'MONTHLY CHANGE', 'ANNUAL CHANGE')
        setList = [yahoo, tradingview, dow]
        setup = default_setup

        yahoo_path = '//*[@id="scr-res-table"]/div[1]/table/tbody/tr['
        tradingview_path = '//*[@id="js-screener-container"]/div[@class="tv-screener__content-pane"]/table/tbody/tr['
        dow_path = '//*[@id="tablepress-36"]/tbody/tr['
        xpaths = [yahoo_path, tradingview_path, dow_path]
        pathing = '//tr['

        yahoo_param = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        trad_param = [4, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        dow_param = [1, 2, 3, 4, 5, 6, 7]
        param = [0]
        params = [yahoo_param, trad_param, dow_param]

        for i in range(len(mainNames)):
            if (mainNames[i] in url):
                fileName = mainNames[i] + '.csv'
                setup = setList[i]
                pathing = xpaths[i]
                param = params[i]
                i += len(mainNames)

        csvExists = path.exists(fileName)
        file = open(fileName, 'w+', encoding='UTF-8')
        csvFile = csv.writer(file)
        if (not csvExists):
            csvFile.writerow(setup)

        j = 1
        next = True

        while next:
            num = str(j)
            string = pathing + num + ']//text()'
            element = response.xpath(string).extract()

            if (element == []):
                next = False
            else:
                arr = []
                for i in range(len(element)):
                    if i in param:
                        arr += [element[i]]
                csvFile.writerow(tuple(arr))
                j += 1

        file.close()
