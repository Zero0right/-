# -*- coding = utf-8 -*-
# @Time: 2022/1/11 14:24
# @Author: Zero_Right
# @File: testWordCloud.py
# @Software: PyCharm

import jieba                            #分词
from matplotlib import pyplot as plt    #绘图，科研，类似echarts
from wordcloud import WordCloud         #词云
from PIL import Image                   #图片处理
import numpy as np                      #矩阵运算
import sqlite3                          #数据库

#获取词
connect=sqlite3.connect("doubanTop250.db")
cursor=connect.cursor()
sql='''
    select quote from movie
'''
data=cursor.execute(sql)
text=""
for temp in data:
    text=text+temp[0]
cursor.close()
connect.close()

#利用jieba分词
cut=jieba.cut(text)
string=" ".join(cut)
#print(string)
print(len(string))

#设置词云背景
img=Image.open(r'.\static\assets\img\anime.png')
img_array=np.array(img)
wc=WordCloud(
    background_color="white",
    mask=img_array,
    font_path="HGLB_CNKI.TTF" #字体路径，在C\Windows
)
wc.generate_from_text(string)

#绘制
fig=plt.figure(1)
plt.imshow(wc)
plt.axis("off")
#plt.show()
plt.savefig(r".\static\assets\img\result.png",dpi=500)