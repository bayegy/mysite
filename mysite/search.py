
# -*- coding: utf-8 -*-

# from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from . import mysql
# 表单


def main(request):
    return render_to_response('main.html')

# 接收请求数据


def search(request):
    db = mysql.Mysql("localhost", "root", "947366", "wstdb_academic")
    request.encoding = 'utf-8'
    input_word = request.GET['q'].strip()
    df = db.select("tb_papers", condition="发表日期='{}'".format(input_word))
    del df["索引"]
    context = {}
    context['table1'] = df.to_html()
    return render_to_response('search-result.html', context)
