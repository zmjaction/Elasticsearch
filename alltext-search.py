# encoding: utf-8
__author__ = 'action'
"""
借鉴: https://cuiqingcai.com/6214.html

"""
from elasticsearch import Elasticsearch
es = Elasticsearch()
import json

dsl = {
    'query':{
        'match':{
            'title': '中国 领事馆'
        }
    }
}


result = es.search(index='news', doc_type='politics', body=dsl)
print(json.dumps(result, indent=2, ensure_ascii=False))

result = es.search(index='news', doc_type='politics')
print(result)
print(json.dumps(result, indent=2, ensure_ascii=False))

