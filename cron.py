# -*- coding:utf-8 -*-
#加载模块，此处大致按功能划分行，是为了能够更方便理解代码
#语法格式 python cron.py semwatch.org keywords.txt
import sys, os, random, time, datetime, StringIO, re, string
from BeautifulSoup import BeautifulSoup
import urllib, re
import curl

def getRank(strHtml, strDomain):
    soup=BeautifulSoup(strHtml)
    for i in range(1,101):
        getstr=soup.findAll('table',id=i)
        tmpstr=str(getstr).replace('<b>','')
        tmpstr=tmpstr.replace('</b>','')
        if(string.rfind(tmpstr,strDomain)!=-1):
            rank=i
            break
        else:
            rank='-'
    return rank

#sys.argv是系统参数，1:3切片意味着读取参数2，3，分别赋值给两个变量
site, file_keyword = sys.argv[1:3]
keywords = [] #先将keywords声明初始为列表型变量
#迭代文件，每次读取一行文字
for line in open(file_keyword):
    line = line.rstrip() #将行尾的空白字符去掉，一般行尾会有换行符等
    if line:#判断该行是否是空白行，也可更标准的写作if len（line）！=0：
        keywords.append(line) #将读取到的文字加入到keywords列表中
#获取UTC时间，之所以使用UTC时间是为了避免时区问题带来的未知麻烦
#北京时间是UTC+8，如该日UTC时间01:00相当于北京时间09:00
now = datetime.datetime.utcnow()
#将UTC时间格式化，变成如1970-01-01的格式
date = datetime.datetime.strftime(now, '%Y-%m-%d')
#尝试创建文件夹，如果文件夹已创建则跳过
try:
    os.mkdir('rank')
except:
    pass
#打开输出数据的文件，以当日的日期命名它
f = open('%s.csv' % date, 'w')
for keyword in keywords:
#因为关键词可能是非ASCII字符集的，所以需要编码
    encoded_keyword = urllib.quote_plus(keyword)
#下载SERP并提取链接
    url = 'http://www.baidu.com/s?wd=%s&rn=100' % encoded_keyword
#下载SERP，如果出现验证码即延时10分钟并重试
    while True:
        html = curl.curl(url, retry=True, delay=60)
        if '<img src="http://verify.baidu.com/cgi-bin/' in html:
            #except:
            f.write('"%s","%s","%s"\n' % (keyword, 'vertify', '-'))
            continue
        pos=getRank(html,site)
        f.write('"%s","%s","%s"\n' % (keyword, pos, site))
        print keyword, pos
        break
    delay = random.randint(1,2) #随机设定延时时间为1秒或2秒
    time.sleep(delay) #等待x秒以后继续查询下一个词的排名