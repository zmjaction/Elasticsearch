# encoding: utf-8
__author__ = 'action'

"""
借鉴: https://cuiqingcai.com/6214.html

"""

"""
Elasticsearch 更特殊的地方在于其异常强大的检索功能。
对于中文来说，我们需要安装一个分词插件，这里使用的是 elasticsearch-analysis-ik，GitHub 链接为：https://github.com/medcl/elasticsearch-analysis-ik，
这里我们使用 Elasticsearch 的另一个命令行工具 elasticsearch-plugin 来安装，这里安装的版本是 6.2.4，请确保和 Elasticsearch 的版本对应起来，命令如下：

 elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v6.2.4/elasticsearch-analysis-ik-6.2.4.zip


这里的版本号请替换成你的 Elasticsearch 的版本号。

安装之后重新启动 Elasticsearch 就可以了，它会自动加载安装好的插件。

注意: 请确保和 Elasticsearch 的版本对应起来
"""

# 新建索引并指定需要分词的字段
from elasticsearch import Elasticsearch
es = Elasticsearch()
mapping = {
    'properties':{
        'title':{
            'type': 'text',
            'analyzer': 'ik_max_word',
            'search_analyzer': 'ik_max_word'
        }
    }
}

# es.indices.delete(index='news', ignore=[400, 404])
es.indices.create(index='news', ignore=400)
result = es.indices.put_mapping(index='news', doc_type='politics', body=mapping)
print(result)

"""
新建了一个索引，然后更新了它的 mapping 信息，
mapping 信息中指定了分词的字段，指定了字段的类型 type 为 text，
分词器 analyzer 和 搜索分词器 search_analyzer 为 ik_max_word，即使用我们刚才安装的中文分词插件。
如果不指定的话则使用默认的英文分词器。

"""

# 插入测试数据
datas = [
    {
        'title': '美国留给伊拉克的是个烂摊子吗',
        'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm',
        'date': '2011-12-16'
    },
    {
        'title': '公安部：各地校车将享最高路权',
        'url': 'http://www.chinanews.com/gn/2011/12-16/3536077.shtml',
        'date': '2011-12-16'
    },
    {
        'title': '中韩渔警冲突调查：韩警平均每天扣1艘中国渔船',
        'url': 'https://news.qq.com/a/20111216/001044.htm',
        'date': '2011-12-17'
    },
    {
        'title': '中国驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首',
        'url': 'http://news.ifeng.com/world/detail_2011_12/16/11372558_0.shtml',
        'date': '2011-12-18'
    }
]

for data in datas:
    es.index(index='news', doc_type='politics', body=data)
    # 通过index()插入数据

# 查询相关内容
result = es.search(index='news', doc_type='politics')

print(result)

# 进行全文检索,体现elasticsearch搜索引擎特性
# 查看alltext-search.py, 运行


# dsl = {
#     'query':{
#         'match':{
#             'title': '中国 领事馆'
#         }
#     }
# }
#
# es = Elasticsearch()
# result = es.search(index='news', doc_type='politics', body=dsl)
# print(json.dumps(result, indent=2, ensure_ascii=False))











