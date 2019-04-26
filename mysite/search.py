
# -*- coding: utf-8 -*-

# from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from myutils.mysql import Mysql
import os
import re
# 表单
store_file_name = ""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def form_a(links: []):
    return ['<a href="{}">'.format(l) + "查看" + '</a>' for l in links]


def main(request):
    return render_to_response('main.html')

# 接收请求数据


def search(request):
    global store_file_name
    global BASE_DIR
    # user_id = request.session.get('_auth_user_id')
    store_file_name = BASE_DIR + '/static/' + 'search_result_table.txt'
    print("Test at search:")
    db = Mysql("localhost", "root", "947366", "wstdb_academic")
    request.encoding = 'utf-8'

    input_word = request.GET['q'].strip().replace('：', ':')
    if input_word.find(':') == -1:
        condition = "发表日期='{}'".format(input_word)
    else:
        input_word = re.split(':', input_word)
        condition = "发表日期>='{}' and 发表日期<='{}'".format(input_word[0].strip(), input_word[1].strip())
    try:
        # print(condition)
        df = db.select("tb_papers", condition=condition)
        # print(df)
        del df["索引"]
        df.to_csv(store_file_name, encoding='utf-8', sep='\t')
        df['文献网址'] = form_a(df['文献网址'])
        df = df.to_html(escape=False)
    except Exception as e:
        print(e)
        df = '<p>查询结果为空</p>'

    context = {}
    context['table1'] = df
    return render_to_response('search-result.html', context)
