from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Modelinfo(models.Model):
	"""docstring for Modelinfo"""
	authtarget = models.CharField(max_length=100)
	token = models.CharField(max_length=100)
	redir = models.CharField(max_length=100)
	ipaddr = models.CharField(max_length=16)

class Numberinfo(Modelinfo):
	"""docstring for Numberinfo"""
	number = models.CharField(max_length=12)

class nodogsplash(models.Model):
	"""docstring for nodogsplash"""	
	ipAddr = models.CharField(max_length=16)
	macAddr = models.CharField(max_length=30)
	token = models.CharField(max_length=10)
	redir = models.CharField(max_length=100)
	