import re
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

# 获取源码
def getcontent(id, cursor):
    url = "https://video.coral.qq.com/varticle/7535800567/comment/v2?callback=_varticle7535800567commentv2&orinum=10&oriorder=o&pageflag=1&cursor=" + cursor + "&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=132&_=" + str(
        id)
    response = urllib.request.Request(url=url, headers=headers)
    # Requset用于加入头部信息，host名称以及ip等，给request初始化信息,urlopen中不能加
    html = urllib.request.urlopen(response).read().decode("utf-8", "ignore")
    # urlopen发起request的请求，打开网页，也可以给request加一个opener，一般默认的opener就可以了
    # urlopen只能获得一个HTTPResponse对象，要用read函数来读取这个对象中的字符流，得到的字符流用utf-8编码，ignore代表忽略错误处理
    # 相当于得到了打开了这个容器，要用read去读里面的东西
    # 这个html可以用soup进行解析

    return html


# 从源码中获取评论的数据
def getcomment(html):
    pat = '"content":"(.*?)"'
    rst = re.compile(pat, re.S).findall(html)
    # 利用非贪婪模式匹配整个网页中的信息，以”content”:“开头的以”结尾的所有数据，返回括号中的内容，返回的为列表
    # re是正则式匹配模块，compile把正则表达式pat转化成一个对象，然后用这个对象作为规则去findall整个HTTP的代码
    return rst


# 从源码中获取下一轮刷新页的ID
def getcursor(html):
    pat = '"last":"(.*?)"'  # 非贪婪模式匹配：加问号，表示匹配到了符合结果的就返回，.*匹配之后的所有，？表示非贪婪，匹配到第一个"就返回，否则会匹配到这个字符串中最后个"
    lastId = re.compile(pat, re.S).findall(html)[0]  # re.S表示把回车那些全部包括进去，把html中作为一个整体字符串
    return lastId


# 初始页面
id = 1638542168564
# 初始待刷新页面ID
cursor = "686888069855644446"
content = []
for i in range(1, 11):
    html = getcontent(id, cursor)
    # 获取评论数据
    commentlist = getcomment(html)
    print("第" + str(i) + "页评论")
    for j in range(0, len(commentlist)):
        print("第" + str(j + 1) + "条评论：" + str(commentlist[j]))
        # 获取下一轮刷新页ID
        content.append(commentlist[j])
        cursor = getcursor(html)
        id += 1
df = pd.DataFrame(content, columns=['评价'])
df.to_excel('E:/Python/zuoye4/腾讯视频评价.xls')  # 保存文件，数据持久化
