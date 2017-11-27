# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Time(models.Model):
	time = models.CharField(max_length=50, default='DEAFULT')
	date = models.CharField(max_length=50, default='DEAFULT')
