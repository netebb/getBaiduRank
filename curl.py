#coding=utf8
from pycurl import *
import StringIO, time, random

def curl(url, retry=False, delay=1):
    '''Basic usage: curl('http://www.xxx.com/'), will download the url.
    If set `retry` to True, when network error, it will retry automatically.
    `delay` set the seconds to delay between every retry.
    **kwargs can be curl params. For example:
    curl(url, FOLLOWLOCATION=False, USERAGENT='Firefox')
    '''
    useragent_list = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
    'Opera/9.20 (Windows NT 6.0; U; en)',
    'Mozilla/4.0 (compatible; MSIE 5.0; Windows NT 5.1; .NET CLR 1.1.4322)',
    'Opera/9.00 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 8.0',
    'Mozilla/4.0 (compatible; MSIE 6.0; MSIE 5.5; Windows NT 5.1) Opera 7.02 [en]',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20060127 Netscape/8.1',
    ]
    size = len(useragent_list)
    useragent = useragent_list[random.randint(0, size-1)]
    s = StringIO.StringIO()
    c = Curl()
    c.setopt(NOSIGNAL, True)#不超时
    c.setopt(FOLLOWLOCATION, True)#设置为1告诉libcurl遵循任何访问
    c.setopt(MAXREDIRS, 5)#设定重定向的数目限制,设置为-1表示无限的重定向（默认）
    c.setopt(TIMEOUT, 120)
    c.setopt(URL, url)#主机名或IP地址
    c.setopt(WRITEFUNCTION, s.write)#写(下载)回传函数,传递一个写指针供外部操作, 一次回调内容大小在 CURL_MAX_WRITE_SIZE (curl.h头文件)中设置
    c.setopt(USERAGENT, useragent)#伪造USERAGENT
    while 1:
            try:
                c.perform()
                break
            except:
                if retry:
                    time.sleep(delay)
                else:
                    return False
    return s.getvalue()