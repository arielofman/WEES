# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import Customer

class Coupon(models.Model):
	coupon_code = models.CharField(unique=True, max_length=150)
	customer_fk = models.ForeignKey(Customer, on_delete=models.CASCADE)
	date_created = models.DateTimeField()
	redeemed = models.BooleanField(default=False)
	date_redeemed = models.DateTimeField(null=True)
	start_date = models.DateTimeField()
	expires = models.DateTimeField()

	def __str__(self):
		return self.coupon_code

	class Meta:
		db_table = 'QRCoupons'