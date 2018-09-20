# encoding: utf-8
__author__ = 'action'
__date__ = '20/09/18 上午 09:10'

"""
借鉴: https://cuiqingcai.com/6214.html

"""

from elasticsearch import Elasticsearch

es = Elasticsearch()  # 默认是localhost
# es = Elasticsearch(['127.0.0.1:9200'])  # 可以指定ip
# es = Elasticsearch(
#     ['localhost', 'otherhost'],
#     http_auth=('user', 'secret'),
#     scheme="https",
#     port=443,
# )
result = es.indices.create(index='news', ignore=400)
print(result)

"""
 ignore 参数为 400，这说明如果返回结果是 400 的话，就忽略这个错误不会报错，程序不会执行抛出异常。
 如果不加程序的执行就会出现问题，所以说，我们需要善用 ignore 参数，把一些意外情况排除，这样可以保证程序的正常执行而不会中断
 
"""

