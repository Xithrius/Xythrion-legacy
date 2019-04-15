from lxml import html
import requests


def get_stock_summary(abbreviation, option='low'):
    page = requests.get(f'https://finance.yahoo.com/quote/{abbreviation}?p={abbreviation}&.tsrc=fin-srch')
    tree = html.fromstring(page.content)

    title = tree.xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1/text()')
    percentage = tree.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]/text()')
    open = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[2]/td[2]/span/text()')
    previous_close = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]/span/text()')
    bid = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[3]/td[2]/text()')
    ask = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[4]/td[2]/text()')
    range_day = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[5]/td[2]/text()')
    range_52_week = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[6]/td[2]/text()')
    market_cap = tree.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[1]/td[2]/span/text()')
    one_year_target_est = tree.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[8]/td[2]/span/text()')

    stock_dict = {}

    stock_dict['Title'] = title
    stock_dict['Percentage change'] = percentage
    stock_dict['Open'] = open
    stock_dict['Previous close'] = previous_close
    stock_dict['Ask'] = ask
    stock_dict['Bid'] = bid
    stock_dict["Today's range"] = range_day
    stock_dict['52 week range'] = range_52_week
    stock_dict['Market cap'] = market_cap
    stock_dict['1 year target estimate'] = one_year_target_est

    if option == 'advanced':
        volume_day = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[7]/td[2]/span/text()')
        volume_avg = tree.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[8]/td[2]/span/text()')
        beta_3y_monthly = tree.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[2]/td[2]/span/text()')
        pe_ratio_ttm = tree.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[3]/td[2]/span/text()')
        eps_ttm = tree.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[4]/td[2]/span/text()')
        earnings_date = tree.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[5]/td[2]/text()')
        forward_dividend_and_yield = tree.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[6]/td[2]/text()')
        ex_dividend_date = tree.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[7]/td[2]/span/text()')

        stock_dict['Volume'] = volume_day
        stock_dict['Average volume'] = volume_avg
        stock_dict['Beta (3Y Monthly)'] = beta_3y_monthly
        stock_dict['PE Ratio (TTM)'] = pe_ratio_ttm
        stock_dict['EPS (TTM)'] = eps_ttm
        stock_dict['Earnings Date'] = earnings_date
        stock_dict['Forward Dividend & Yield'] = forward_dividend_and_yield
        stock_dict['Ex-Dividend Date'] = ex_dividend_date

    return stock_dict
