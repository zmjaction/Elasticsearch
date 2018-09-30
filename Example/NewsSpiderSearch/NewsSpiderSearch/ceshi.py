# encoding: utf-8
__author__ = 'action'


import requests
from scrapy.selector import Selector
from urllib.parse import urljoin
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',

}

url = 'http://news.sina.com.cn/c/2018-09-25/doc-ihkmwytp0800594.shtml'
response = requests.get(url, headers=headers)
# print(response)
# response.encoding='utf-8'
# content = response.text[4:-12]
# results = content[content.index('(') + 1:-2]
# # res = results.replace('\\', '')
# result = json.loads(results)
#
# print(result['result']['data'])


# print(res)
# print(result)

selector = Selector(text=response).xpath('//*[@id="divCsLevel_0"]/*')
