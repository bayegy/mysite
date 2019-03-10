import requests
from lxml import html
import re


class Translator(object):
    """Translate english to chinese"""

    def __init__(self):
        self.__url = "http://www.youdao.com/w/{}/#keyfrom=dict2.top"

    def translate(self, wd):
        url = self.__url.format(wd)
        try:
            results = requests.get(url)
        except Exception as e:
            print(e)
        tree = html.fromstring(results.text)
        chinese = tree.xpath("//div[@class='trans-container']/ul/li/text()")
        try:
            chinese = chinese if chinese else tree.xpath("//div[@class='trans-container']/p/text()")[1]
        except Exception:
            chinese = tree.xpath("//p[@class='wordGroup']/text()")

        out = chinese if isinstance(chinese, str) else '//'.join([w.strip() for w in chinese]).strip('/')

        return re.sub('/+', '//', out)
