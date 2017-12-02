#coding=utf-8
from django.utils import timezone
import urllib2
from bs4 import BeautifulSoup
import re
import time
from models import Time
from celery import app


@app.task
def spider(word):
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    }
    data = None
    start = time.time()
    start_str =  time.strftime("%Y-%m-%d %X")

    content = []
    ###############
    dic = {word:[]}

    url = 'https://www.baidu.com/s?ie=utf-8&wd='+word
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response.read(), "html.parser")
    a_tags = soup.select('div.result h3.t > a')

    for tag in a_tags:
        res = r'<a.*?>(.*?)</a>'
        raw_content = re.findall(res, str(tag), re.S|re.M)[0]
        #################
        dic[word].append(raw_content.replace('<em>', '').replace('</em>', ''))
    
    end = time.time()
    end_str =  time.strftime("%Y-%m-%d %X")

    time_duration = ['TimeDuration: '+str(round(end-start,2))+'s',start_str,end_str,' ']
    dic[word] = time_duration + dic[word]
    #################
    content.append(dic)

    return content

def spider_2(word):
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    }
    data = None
    start = time.time()
    start_str =  time.strftime("%Y-%m-%d %X")

    content = []
    dic = {word:[]}
    url = 'https://www.baidu.com/s?ie=utf-8&wd='+word
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response.read(), "html.parser")
    a_tags = soup.select('div.result h3.t > a')

    for tag in a_tags:
        res = r'<a.*?>(.*?)</a>'
        raw_content = re.findall(res, str(tag), re.S|re.M)[0]
        dic[word].append(raw_content.replace('<em>', '').replace('</em>', ''))
    
    end = time.time()
    end_str =  time.strftime("%Y-%m-%d %X")

    time_duration = ['TimeDuration: '+str(round(end-start,2))+'s',start_str,end_str,' ']
    dic[word] = time_duration + dic[word]
    
    content.append(dic)
    return content
	
@app.task    		
def getTime():
    now = time.strftime("%X")
    today = time.strftime("%Y-%m-%d")
    Time.objects.create(time=now, date=today)


def showTime():
    today = time.strftime("%Y-%m-%d")
    items = Time.objects.filter(date=today)
    result = []
    j=0
    for i in items:
        result.insert(0, i.date+' '+i.time+'<br>')
    result = result[:50]
    return result

@app.task 
def timeKiller():
    key_words = ['django', 'celery', 'BeautifulSoup',
                're', 'urllib2','Request','linux','pycharm']

    for word in key_words:
        spider_2(word)



