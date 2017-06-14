# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
 
class Customer(models.Model): 
	ip_address = models.CharField(max_length=50)
	refresh = models.DateTimeField() 

	def __str__(self):
		return self.ip_address

	class Meta:
		db_table = 'Customers'