from scrapy.selector import Selector
import requests
from pprint import pprint
import re
import string

BASE_URL = 'https://www.worldcoinindex.com'
COIN_URL = "%s/trending/overview" % BASE_URL

FIELD_MAP = {
    2: 'name',
    3: 'symbol',
    4: 'price',
    5: '%',
    6: '%7d',
    7: '%30d',
    8: '%90d',
    9: '%180d',
    10: '%365d',
    11: 'number_coins',
    12: 'market_cap',
    13: 'rank'
}


def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def to_float(val):
    stripped_val = val.strip(string.punctuation).strip(',')
    if val[0] == '-':
        stripped_val = '-' + stripped_val
    try:
        return round(float(stripped_val), 2)
    except Exception as e:
        print("Error converting %s: %s" % (stripped_val, e))
        return stripped_val


def get_coin_map():
    r = requests.get(COIN_URL)
    doc = r.text
    sel = Selector(text=doc, type="html")
    coin_rows = sel.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "coinzoeken", " " ))]')
    coins = []
    for i, row in enumerate(coin_rows):
        cols = row.xpath(".//td")
        obj = {}
        for col, td in enumerate(cols):
            val = clean_html(td.extract())
            if col in FIELD_MAP:
                key = FIELD_MAP[col]
                if '%' in key or key == 'price':
                    val = to_float(val)
                obj[key] = val
        coin_name = obj['name']
        obj['url'] = '%s/coin/%s' % (BASE_URL, coin_name)
        coins.append(obj)
    return coins


if __name__ == '__main__':
    coin_map = get_coin_map()
    pprint(coin_map)
