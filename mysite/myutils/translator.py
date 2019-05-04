import requests
from lxml import html
import re
# from myutils.net import Net
import os
import time
import hashlib
import random
import json


class Translator(object):
    """Translate english to chinese"""

    def __init__(self):
        # self.base=os.path.dirname(os.path.dirname(__file__))
        self.__url = "http://www.youdao.com/w/{}/#keyfrom=dict2.top"
        self.__post_url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
        # self.net=Net(protocol='http',post_headers=self.base+'/config/youdao_post_header.conf')

    def translate(self, wd):
        url = self.__url.format(wd.strip())
        try:
            results = requests.get(url)
        except Exception as e:
            print(e)
        tree = html.fromstring(results.text)
        # breakpoint()
        chinese = tree.xpath("//div[@class='trans-container']/ul/li/text()")
        try:
            chinese = chinese if chinese else tree.xpath("//div[@class='trans-container']/p/text()")[1]
        except Exception:
            chinese = tree.xpath("//p[@class='wordGroup']/text()")

        out = chinese if isinstance(chinese, str) else '//'.join([w.strip()
                                                                  for w in chinese]).strip('/').replace("\n", "").replace(" ", "")

        return re.sub('/+', '//', out)

    def translate_paragraph(self, paragraph):
        """
        paragraph: the paragraph you want to translate
        """
        paragraph = paragraph.strip()
        i = str(int(time.time() * 1000) + random.randint(1, 10))
        src = "fanyideskweb" + paragraph + i + "@6f#X3=cCuncYssPsuRUE"
        m2 = hashlib.md5()
        m2.update(src.encode())
        str_sent = m2.hexdigest()

        head = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            # 'Content-Length':'5',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'fanyi.youdao.com',
            'Origin': 'http://fanyi.youdao.com',
            'Referer': 'http://fanyi.youdao.com/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            # 'Cookie': 'YOUDAO_MOBILE_ACCESS_TYPE=1; OUTFOX_SEARCH_USER_ID=833904829@10.169.0.84; OUTFOX_SEARCH_USER_ID_NCOO=1846816080.1245883; fanyi-ad-id=39535; fanyi-ad-closed=1; JSESSIONID=aaaYuYbMKHEJQ7Hanizdw; ___rl__test__cookies=1515471316884'
        }
        head['Cookie'] = 'OUTFOX_SEARCH_USER_ID=833904829@10.169.0.84; OUTFOX_SEARCH_USER_ID_NCOO=1846816080.1245883;  ___rl__test__cookies=' + \
            str(time.time() * 1000)
        # '___rl__test__cookies=1515471316884'

        data = {
            'i': paragraph,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': i,
            'sign': str_sent,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION',
            'typoResult': 'false'
        }

        s = requests.session()
        # print data
        url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        p = s.post(url, data=data, headers=head)
        js = json.loads(p.text)
        # breakpoint()
        try:
            res = [d["tgt"] for d in js["translateResult"][0]]
            return ''.join(res)
        except IndexError:
            return ""


    def translate_date(self, date):
        dt = self.translate_paragraph(date).replace(
            '日', '').replace('年', '-').replace('月', '-').strip('-|,') if date else ""
        dt = re.findall('\d{4}-\d{1,2}-\d{1,2}', dt)
        return dt.pop() if dt else ""
