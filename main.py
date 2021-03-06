#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request, Response,render_template
from run_spider import remove_duplicate, get_cursors
import os
import json
import logging


#                       _oo0oo_
#                      o8888888o
#                      88" . "88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |// '.
#                 / \\|||  :  |||// \
#                / _||||| -:- |||||- \
#               |   | \\\  -  /// |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          ."" '<  `.___\_<|>_/___.' >' "".
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#         \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/___.-`___.-'=====
#                       `=---='
#
#
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#               佛祖保佑         永无BUG


app = Flask(__name__)

"""首页"""
@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')


"""问题页"""
@app.route('/answer', methods=['GET'])
def answer():
    return render_template('answer.html')


"""搜索"""
@app.route('/search', methods=['POST'])
def search():
    question = request.form['question']

    logging.info("Get the search: %s" % question)

    """将问题传到爬虫并返回爬虫结果"""
    remove_duplicate(question)
    os.system(r'python run_spider.py "{}"'.format(question))
    cursors = get_cursors(question)


    """返回爬虫结果"""
    result = {}

    # CSDN结果
    result['csdn'] = []
    index = 0

    for doc in cursors['csdn']:
        result['csdn'].append({})
        result['csdn'][index]['question'] = doc['topic']
        result['csdn'][index]['answer'] = [doc['answer']]
        index += 1

    # Stackoverflow结果
    result['stackoverflow'] = []
    index = 0

    for doc in cursors['stackoverflow']:
        result['stackoverflow'].append({})
        result['stackoverflow'][index]['question'] = doc['topic']
        result['stackoverflow'][index]['description'] = doc['question']
        result['stackoverflow'][index]['answer'] = doc['answers']
        index += 1

    # V2EX结果
    result['v2ex'] = []
    index = 0

    for doc in cursors['v2ex']:
        result['v2ex'].append({})
        result['v2ex'][index]['question'] = doc['topic']
        result['v2ex'][index]['description'] = doc['question']
        result['v2ex'][index]['answer'] = doc['answers']
        index += 1

    # V2EX结果
    result['oschina'] = []
    index = 0

    for doc in cursors['oschina']:
        result['oschina'].append({})
        result['oschina'][index]['question'] = doc['topic']
        result['oschina'][index]['description'] = doc['question']
        result['oschina'][index]['answer'] = doc['answers']
        index += 1

    # Zhihu结果
    result['zhihu'] = []
    index = 0

    for doc in cursors['zhihu']:
        result['zhihu'].append({})
        result['zhihu'][index]['question'] = doc['topic']
        result['zhihu'][index]['description'] = doc['question']
        result['zhihu'][index]['answer'] = doc['answers']
        index += 1

    return Response(json.dumps(result), headers={'Access-Control-Allow-Origin': '*'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
