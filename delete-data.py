# encoding: utf-8
__author__ = 'action'

"""
借鉴: https://cuiqingcai.com/6214.html

"""

from elasticsearch import Elasticsearch
es = Elasticsearch()

result = es.delete(index='news', doc_type='politics', id=1)

"""
如果想删除一条数据可以调用 delete() 方法，指定需要删除的数据 id 即可
可以看到运行结果中 result 字段为 deleted，代表删除成功，_version 变成了 3，又增加了 1。


"""

print(result)
