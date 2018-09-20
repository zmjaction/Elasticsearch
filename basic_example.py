# encoding: utf-8
__author__ = 'action'

"""
借鉴:https://github.com/Germey/ElasticSearch/blob/master/basic_example.py
"""

from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch()

# 插入的_source內容
doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}
res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
print(res)
print(res['result'])

# 两种查询方法get() search()
res = es.get(index="test-index", doc_type='tweet', id=1)   # get()可以指定id查询
result = es.search(index="test-index", doc_type='tweet')  # search()查询所有
# print(res['_source'])
# print('*'*10)
# print(result)
es.indices.refresh(index="test-index")  # 刷新

res = es.search(index="test-index", body={"query": {"match_all": {}}})  # search()查询所有
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print('11111111111111')
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])