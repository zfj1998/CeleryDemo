# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from task import spider,spider_2

import time


def celery(request):
	start = time.time()

	key_words = ['django', 'celery', 'BeautifulSoup',
	   			're', 'urllib2', 'Request','linux','pycharm',
	               'git', 'bootstrap', 'ajax', 'jquery',
	               'views' ,'django-celery', 'models']

	infos = []
	works = []
	for word in key_words:
		works.append(spider.delay(word))
	for work in works:
		infos.extend(work.get())

	end = time.time()
	infos = [{'Time Cost':[str(round(end-start,2))+'s']}] + infos
	return render(request, 'home.html',{'infos':infos})

def show_celery(request):
	key_words = ['django', 'celery', 'BeautifulSoup',
	   			're', 'urllib2', 'Request','linux','pycharm',
	               'git', 'bootstrap', 'ajax', 'jquery',
	               'views' ,'django-celery', 'models']
	infos = []
	for word in key_words:
		infos.append(spider.delay(word))
		infos.append('<br>')
	return HttpResponse(infos)

def slow_celery(request):
	start = time.time()

	key_words = ['django', 'celery', 'BeautifulSoup',
	   			're', 'urllib2', 'Request','linux','pycharm',
	               'git', 'bootstrap', 'ajax', 'jquery',
	               'views' ,'django-celery', 'models']

	infos = []
	for word in key_words:
		infos.extend(spider.delay(word).get())

	end = time.time()
	infos = [{'Time Cost':[str(round(end-start,2))+'s']}] + infos
	return render(request, 'home.html',{'infos':infos})

def compare(request):
	start = time.time()

	key_words = ['django', 'celery', 'BeautifulSoup',
	   			're', 'urllib2', 'Request','linux','pycharm',
	               'git', 'bootstrap', 'ajax', 'jquery',
	               'views' ,'django-celery', 'models']

	infos = []
	for word in key_words:
		infos.extend(spider(word))
	
	end = time.time()
	infos = [{'Time Cost':[str(round(end-start,2))+'s']}] + infos
	return render(request, 'home.html',{'infos':infos})
