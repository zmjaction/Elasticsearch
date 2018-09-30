from django.shortcuts import render

# Create your views here.
import pickle
from django.shortcuts import render
import json

from django.utils.datastructures import OrderedSet
from django.views.generic.base import View
from search.models import SinaIndex
from django.http import HttpResponse
from datetime import datetime
import redis
from elasticsearch import Elasticsearch   # elasticsearch-dsl 是对elasticsearch进一步的封装,但是elasticsearch也可以直接使用

client = Elasticsearch(hosts=["localhost"])
# 使用redis实现top-n排行榜
redis_cli = redis.StrictRedis()


class IndexView(View):
    """首页get请求top-n排行榜"""
    # 首页

    @staticmethod
    def get(request):
        topn_search_clean = []
        topn_search = redis_cli.zrevrangebyscore(
            "search_keywords_set", "+inf", "-inf", start=0, num=5)
        for topn_key in topn_search:
            topn_key = str(topn_key, encoding="utf-8")
            topn_search_clean.append(topn_key)
        topn_search = topn_search_clean
        return render(request, "index.html", {"topn_search": topn_search})


class SearchSuggest(View):
    """搜索建议"""

    def get(self, request):
        key_words = request.GET.get('s', '')
        # current_type = request.GET.get('s_type', '')
        # if current_type == "sinaarticle":
        return_suggest_list = []
        if key_words:
            s = SinaIndex.search() # 创建一个对象,在SinaIndex中已经连接es
            """fuzzy模糊搜索, fuzziness 编辑距离, prefix_length前面不变化的前缀长度"""
            # 编辑距离(百度下) 就是字符串之间相似程度的计算方法 linux linx
            # 相邻字符串交换位置的最少交换次数
            # match 就不能进行模糊搜索,比如搜索python,不能使用pytho进行
            s = s.suggest('my_suggest', key_words, completion={
                "field": "suggest", "fuzzy": {
                    "fuzziness": 2
                },
                "size": 10
            })
            suggestions = s.execute()
            for match in suggestions.suggest.my_suggest[0].options:
                source = match._source
                return_suggest_list.append(source["NewsTitle"])
        return HttpResponse(json.dumps(return_suggest_list),content_type="application/json")


class SearchView(View):
    """
    搜索
    """

    def get(self, request):
        key_words = request.GET.get("q", "") # 搜索关键词 function add_search()

        # 通用部分
        # 实现搜索关键词keyword加1操作
        redis_cli.zincrby("search_keywords_set", key_words)  # # redis> ZINCRBY salary 2000 tom   # tom 加薪啦！"4000"
        # 获取topn个搜索词
        topn_search_clean = []
        topn_search = redis_cli.zrevrangebyscore(     #  # ZREVRANGEBYSCORE 返回有序集合中指定分数区间内的成员，分数由高到低排序。
            "search_keywords_set", "+inf", "-inf", start=0, num=5)
        for topn_key in topn_search:
            topn_key = str(topn_key, encoding="utf-8")
            topn_search_clean.append(topn_key)
        topn_search = topn_search_clean
        # 获取新闻数量

        sinanews_count = redis_cli.get("sinanews_count")
        if sinanews_count:
            sinanews_count = pickle.loads(sinanews_count)
            # pickle模块的作用: 将字典、列表、字符串等对象进行持久化，存储到磁盘上，方便以后使用
            # pickle.loads(string) 从string中读出序列化前的obj对象
        else:
            sinanews_count = 0
        # 当前要获取第几页的数据
        #  实现热门搜索
        page = request.GET.get("p", "1")
        try:
            page = int(page)
        except BaseException:
            page = 1
        response = []
        start_time = datetime.now()
        s_type = request.GET.get("s_type", "")  # 获取分类信息
        if s_type == "sinaarticle":
            response = client.search(
                index="sinanews",
                request_timeout=60,
                body={
                    "query": {
                        "multi_match": {  # 对多个字段进行搜索multi_match
                            "query": key_words,
                            "fields": ["SourceCategory", "NewsTitle", "NewsContent"]  # 需要搜索的字段
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10,  # 显示10条数据
                    "highlight": {  # 做高亮处理
                        "pre_tags": ['<span class="keyWord">'], # css会自动标红
                        "post_tags": ['</span>'],
                        "fields": {
                            "NewsTitle": {}, # 指定需要做高亮的部分
                            "NewsContent": {},
                        }
                    }
                }
            )
        else:
            pass
        end_time = datetime.now()
        last_seconds = (end_time - start_time).total_seconds()

        # 新浪新闻的具体的信息
        hit_list = []
        error_nums = 0
        if s_type == "sinaarticle":
            for hit in response["hits"]["hits"]:
                hit_dict = {}
                try:
                    if "NewsTitle" in hit["highlight"]:
                        hit_dict["NewsTitle"] = "".join(hit["highlight"]["NewsTitle"])
                    else:
                        hit_dict["NewsTitle"] = hit["_source"]["NewsTitle"]
                    if "NewsContent" in hit["highlight"]:
                        hit_dict["NewsContent"] = "".join(
                            hit["highlight"]["NewsContent"])
                    else:
                        hit_dict["NewsContent"] = hit["_source"]["NewsContent"][:200]
                    hit_dict["create_date"] = hit["_source"]["InsertDate"]
                    hit_dict["NewsRawUrl"] = hit["_source"]["NewsRawUrl"]
                    hit_dict["score"] = hit["_score"]
                    hit_dict["source_site"] = "新浪新闻"
                    hit_list.append(hit_dict)
                except:
                    error_nums = error_nums + 1
        else:
            pass
        total_nums = int(response["hits"]["total"]) # 获取共有总的数量

        # 计算出总页数
        if (page % 10) > 0:
            page_nums = int(total_nums / 10) + 1
        else:
            page_nums = int(total_nums / 10)
        return render(request, "result.html", {"page": page,
                                               "all_hits": hit_list,
                                               "key_words": key_words,
                                               "total_nums": total_nums,
                                               "page_nums": page_nums,
                                               "last_seconds": last_seconds,
                                               "topn_search": topn_search,
                                               "sinanews_count": sinanews_count,
                                               "s_type": s_type,
                                               })


