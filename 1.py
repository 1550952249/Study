import pandas as pd
import pymssql
import requests
from bs4 import BeautifulSoup
import time
import random



url = 'https://movie.douban.com/top250'
a = []  # a用于保存排名
a1 = []  # a1保存电影名字
a2 = []  # a2保存电影评分、导演等信息
a3 = [] #电影简介信息

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'}  # 伪装爬虫
# 豆瓣网禁爬虫代理，要利用header进行伪装
for i in range(0, 250, 25):  # 这个网页每页有25个记录，一共10页，利用for遍历这10页
    # 通过观察豆瓣网页发现每一页的网址中start可以作为每页的网址标识
    time.sleep(random.random() * 3)
    S=requests.session()
    S.keep_alive = False#杀死多余的连接，在多次访问后建立的连接没有关闭，多了后会报错，服务器负载过重，无法建立更多的链接。
    S.headers = headers
    html = S.get(url, params={'start': i}, headers=headers)  # 得到访问url的响应内容，里面包括页面内容
    # html是一个respond类型对象，不是内容，不能进行解析
    soup = BeautifulSoup(html.text, 'html.parser')  # 利用html.parser解析器进行解析,需要对html.content或者html的text进行解析，不然报错
    # 通过查看豆瓣Top250网页的html结构，每个电影的排序存放在body-div class="pic"中的em标签的text中，soup.find_all方法提供CSS类名搜索（字典类型），参数是**kwargs
    # 通过查看豆瓣Top250网页的html结构，每个电影的名字存放在body-div class="hd"中的a标签的第一个span标签中
    # 电影评分、导演、简介等信息都在body-div class="bd"中
    a += soup.find_all('div', class_='pic')  # soup.find_all返回列表类型
    a1 += soup.find_all('div', class_='hd')
    a2 += soup.find_all('div', class_='bd')
    del a2[0 + i]  # 因为每个页面的div，class=‘bd'的标签有2个，把第一个删除
    for x in range(0, 25):  # 电影简介信息没有在网页TOP250中，要进入电影信息页面，利用selenium模拟点击行为进入，然后获取电影简介
        url1 = a[x].contents[3].attrs['href']
        html1 = S.get(url1, headers=headers)
        soup = BeautifulSoup(html1.text, 'html.parser')
        a5 = []
        a5 += (soup.find_all('div', class_='indent', id='link-report'))  # 利用列表存放response对象
        a3.append(''.join(a5[0].text.split()))  # 存放的不只是简介信息。在简介信息前后有回车，读入后造成非期望保存
        # 利用split方法之后可以有效消除字符串中的空白，但是是列表形式，要转为字符串o



film_rand = []
film_name = []
film_maker = []
film_score = []
film_info = []
film_actor = []
for i in a:
    film_rand.append(i.contents[1].contents[0].text)  # 通过加断点调试查看变量在内存中的保存，依次寻找树结构中的值
for i in a1:
    film_name.append(i.contents[1].contents[1].text)
for i in a2:
    str = i.contents[1].contents[0]
    str = str.split();#通过split方法返回的结果为列表
    str = ''.join(str)  # 列表转为字符串
    str = str.split("主演");
    film_maker.append(str[0])  # 在网页中演员表和导演属于一个文本字符串
    if len(str) > 1:#如果分隔后只有一个元素代表没有分隔成功，没有对关键字主演进行分隔
        film_actor.append(str[1])
    else:
        film_actor.append("主演信息不全")
    film_score.append(i.contents[3].contents[3].contents[0])
for i in a3:
    film_info.append(i)
film = []
for i in range(0, 250):
    film.append([film_rand[i], film_name[i], film_score[i], film_maker[i], film_actor[i], film_info[i]])
df = pd.DataFrame(film, columns=['排名', '电影名', '评分', '导演', '主演', '简介'])
df.to_excel('E:/Python/zuoye4/豆瓣电影数据.xls')  # 保存文件，数据持久化



def conn():
    connect = pymssql.connect('(local)', 'sa', 'night123', 'pyhton1-1')  # 服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
    return connect


conn = conn()
cursor = conn.cursor()
for i in film:
    if i[3].__contains__("'"):
        i[3] = i[3].replace("'", "‘")
    if i[4].__contains__("'"):
        i[4] = i[4].replace("'", "’")#进行转义字符处理，在sql语句的单引号有歧义，不符合sql语法，sql中两个单引号代表转义的一个单引号，但是在Python中两个单引号被存储的时候不能作为两个单引号，而是作为两个转义单引号 '\'\ 虽然可以输出为两个单引号，但是作为sql均有语法错误，因此在Python中不能成功转义存储两个单引号，把单引号换成‘
    if i[5].__contains__("'"):
        i[5] = i[5].replace("'", "‘")
    sql = "insert into dbo.filmTOP250(film_rand,film_name,film_score,film_maker,film_actor,film_info) values('"+i[0]+"','"+i[1]+"','"+i[2]+"','"+i[3]+"','"+i[4]+"','"+i[5]+"')"
    cursor.execute(sql)
    conn.commit()
print("写入数据库成功")
cursor.close()
conn.close()
