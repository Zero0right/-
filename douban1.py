# -*- coding = utf-8 -*-
# @Time: 2022/1/6 16:19
# @Author: Zero_Right
# @File: douban1.py
# @Software: PyCharm

from bs4 import BeautifulSoup#网页解析，获取数据
import re #正则表达式，进行文字匹配
import urllib.request,urllib.error #指定url获取网页
import xlwt #进行excel操作
import sqlite3 #进行sqlite数据库处理

def main():
    baseurl="https://movie.douban.com/top250?start="
    #获取数据
    datalist=getdata(baseurl)
    #保存数据
    savepathDB="doubanTop250.db"
    #savepath=".\\doubanTop250.xls"
    #savedata(datalist,savepath)
    savedata2(datalist,savepathDB)
#定义正则表达式
#影片链接
findLink=re.compile(r'<a href="(.*?)">')
#图片
findImg=re.compile(r'<img alt=".*src="(.*?)".*"/>',re.S)#忽视换行符
#电影名
findName=re.compile(r'<span class="title">(.*?)</span>')
#影片详情
findInfo=re.compile(r'<p class="">(.*?)</p>',re.S)
#影片评分
findRating_num=re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
#评价人数
findNum=re.compile(r'<span>(.*?)人评价</span>')
#影片概括
findQuote=re.compile(r'<span class="inq">(.*?)</span>')

def getdata(baseurl):
    datalist=[]
    #获取豆瓣10个网页的数据
    for i in range(0,10):
        url=baseurl+str(i*25)
        html=askurl(url)
        #将每一页的html通过bs4解析
        bs=BeautifulSoup(html,"html.parser")
        for item in bs.find_all("div",class_="item"):
            data=[]
            # print(item)
            # break
            item=str(item)

            link=re.findall(findLink,item)[0]
            data.append(link)

            image=re.findall(findImg,item)[0]
            data.append(image)

            name=re.findall(findName,item)
            if len(name)==2:
                cname=name[0]
                data.append(cname)
                fname=name[1].replace("\xa0/\xa0","")
                data.append(fname)
            else:
                data.append(name[0])
                data.append(" ")

            info=re.findall(findInfo,item)[0]
            info=info.replace("\xa0","")
            info=re.sub("<br(\s*)/>(\s*)","",info)
            info=re.sub("/","",info)
            info = re.sub(" ", "", info)
            data.append(info.strip())

            num=re.findall(findNum,item)[0]
            data.append(num)

            rating_num=re.findall(findRating_num,item)[0]
            data.append(rating_num)

            quote=re.findall(findQuote,item)
            if len(quote)!=0:
                quote=quote[0].replace("。", "")
                data.append(quote)
            else:
                data.append(" ")


            datalist.append(data)
            #print(data)
        #解析数据,没获取一个网页就解析，因此在for循环中
    return datalist
'''
def savedata(datalist,savepath):
    print("save.... ")
    workbook=xlwt.Workbook(encoding="utf-8",style_compression=0)    #相当于创建xls文件
    worksheet=workbook.add_sheet("sheet1",cell_overwrite_ok=True)  #建立sheet,对应excel表
    a=("影片链接","图片链接","电影中文名","电影外文名","演员表","评分人数","豆瓣评分","概括")
    for i in range(0,8):
        worksheet.write(0,i,a[i])
    number = 1
    for temp in datalist:
        print("第%d"%(number))
        for j in range(0,8):
            worksheet.write(number,j,temp[j])
        number +=1
    workbook.save(savepath)
'''
def savedata2(datalist,savepathDB):
   init_database(savepathDB)
   print("create the table success...")
   connect=sqlite3.connect(savepathDB)
   cursor = connect.cursor()
   for temp in datalist:
       for i in range(len(temp)):
           if i==5 or i==6:
               continue
           temp[i]='"'+temp[i]+'"'
       sql = '''
            insert into movie(
            movie_link,img_link,chinese_name,foreign_name,information,numberOfEvaluation,rating_num,quote)
            values(%s)'''%",".join(temp)
       print(sql)
       cursor.execute(sql)
       connect.commit()

   cursor.close()
   connect.close()
   print("insert data success...")

#初始化数据库，建表
def init_database(savepathDB):
    connect=sqlite3.connect(savepathDB)
    sql='''
        create table movie
        ( id integer primary key autoincrement,
        movie_link text,
        img_link text,
        chinese_name text,
        foreign_name text,
        information text,
        numberOfEvaluation numeric, 
        rating_num numeric,
        quote text       
        )
    '''
    cursor=connect.cursor()
    cursor.execute(sql)
    connect.commit()
    connect.close()


#获取指定一个网页的源代码（数据）
def askurl(url):
    head={
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36 FS"
    }
    html=""
    req=urllib.request.Request(url=url,headers=head)
    try:
        response=urllib.request.urlopen(req)
        html=response.read().decode("utf-8")
        #print(html)
        return html
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reson"):
            print(e.reson)

if __name__=="__main__":
    main()
    print("finish...")