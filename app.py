# -*- coding = utf-8 -*-
# @Time: 2022/1/11 11:03
# @Author: Zero_Right
# @File: app.py
# @Software: PyCharm

#werkzeug jinja2
from flask import Flask,render_template,request
import datetime
import sqlite3

app=Flask(__name__)

#向html传递数据
#路由解析，通过用户访问的路径，匹配相对的函数
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/index')
def main():
    return render_template("index.html")

@app.route('/movie')
def movie():
    datalist=[]
    connect=sqlite3.connect("doubanTop250.db")
    cursor=connect.cursor()
    sql='''
        select * from movie
    '''
    data=cursor.execute(sql)
    for temp in data:
        datalist.append(temp)
    connect.commit()
    cursor.close()
    connect.close()
    return render_template("movie.html",datalist=datalist)

@app.route('/score')
def score():
    score = []
    num=[]
    connect = sqlite3.connect("doubanTop250.db")
    cursor = connect.cursor()
    sql = '''
            select rating_num,count(rating_num) from movie group by rating_num
        '''
    #data是二维数组（列表）
    data = cursor.execute(sql)
    for temp in data:
        score.append(str(temp[0]))
        num.append(temp[1])
    connect.commit()
    cursor.close()
    connect.close()
    return render_template("score.html",score=score,num=num)

@app.route('/wordcloud')
def wordcloud():
    return render_template("wordcloud.html")

@app.route('/team')
def team():
    return render_template("team.html")

#debug调试模式，修改代码，网页刷新后可以直接改变，不需要重新运行
if __name__=='__main__':
    app.run(debug=True)