# encoding: utf-8
__author__ = 'action'

"""
借鉴: https://cuiqingcai.com/6214.html

"""

from elasticsearch import Elasticsearch

es = Elasticsearch()

es.indices.create(index='news', ignore=400)
data = {'title':'美国留给伊拉克的是个烂摊子吗', 'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm'}

# result = es.create(index='news', doc_type='politics', id=1, body=data)
# 通过create()方法插入数据,需要指明id,
# create() 方法内部其实也是调用了 index() 方法，是对 index() 方法的封装
result = es.index(index='news', doc_type='politics', body=data)
# 通过index()方法插入数据,不指定id,会自动生成一个id



print(result)

"""
这里我们首先声明了一条新闻数据，包括标题和链接，然后通过调用 create() 方法插入了这条数据，在调用 create() 方法时，我们传入了四个参数，
index 参数代表了索引名称，
doc_type 代表了文档类型，
body 则代表了文档具体内容，
id 则是数据的唯一标识 ID。


"""


