# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import Customer

class Coupon(models.Model):
	coupon_code = models.CharField(unique=True, max_length=150)
	ip_address = models.ForeignKey(Customer, on_delete=models.CASCADE)
	date_created = models.DateTimeField()
	redeemed = models.BooleanField(default=False)
	expires = models.DateTimeField()

	def __str__(self):
		return self.coupon_code

	class Meta:
		db_table = 'QRCoupons'