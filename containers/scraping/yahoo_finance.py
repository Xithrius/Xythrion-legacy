'''

+----[ Relay.py ]-------------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


from lxml import html
import requests


"""

Returning stock information from different websites

"""


def get_stock_summary(abbreviation, option='low'):
    """
    Scraping Yahoo finance for stock information
    """
    page = requests.get(f'https://finance.yahoo.com/quote/{abbreviation}?p={abbreviation}&.tsrc=fin-srch')
    tree = html.fromstring(page.content)

    stock_dict = {}

    stock_dict['Title'] = tree.xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1/text()')
    stock_dict['Percentage change'] = tree.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]/text()')
    stock_dict['Open'] = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[2]/td[2]/span/text()')
    stock_dict['Previous close'] = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]/span/text()')
    stock_dict['Ask'] = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[4]/td[2]/text()')
    stock_dict['Bid'] = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[3]/td[2]/text()')
    stock_dict["Today's range"] = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[5]/td[2]/text()')
    stock_dict['52 week range'] = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[6]/td[2]/text()')
    stock_dict['Market cap'] = tree.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[1]/td[2]/span/text()')
    stock_dict['1 year target estimate'] = tree.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[8]/td[2]/span/text()')

    if option == 'advanced':
        stock_dict['Volume'] = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[7]/td[2]/span/text()')
        stock_dict['Average volume'] = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[8]/td[2]/span/text()')
        stock_dict['Beta (3Y Monthly)'] = tree.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[2]/td[2]/span/text()')
        stock_dict['PE Ratio (TTM)'] = tree.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[3]/td[2]/span/text()')
        stock_dict['EPS (TTM)'] = tree.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[4]/td[2]/span/text()')
        stock_dict['Earnings Date'] = tree.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[5]/td[2]/text()')
        stock_dict['Forward Dividend & Yield'] = tree.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[6]/td[2]/text()')
        stock_dict['Ex-Dividend Date'] = tree.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[7]/td[2]/span/text()')

    return stock_dict
