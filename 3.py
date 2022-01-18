import re
import urllib.request

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
url = "https://v.qq.com/x/cover/mzc00200rzjtws6.html"
response = urllib.request.Request(url=url, headers=headers)
html = urllib.request.urlopen(response)
x=html.read().decode('utf-8')
pat = '<span class="units">(.*)</span><span class="decimal">(.*?)</span>'
rst = re.compile(pat, re.S).findall(x)
print(rst)