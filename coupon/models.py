# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import Customer

class ActiveCoupon(models.Model):  
	name = models.CharField(unique=True, max_length=100)
	img_url = models.URLField(max_length=200)
	cover_url = models.URLField(max_length=200)
	active = models.BooleanField(default=False)
	start_date = models.DateTimeField()
	expires = models.DateTimeField()

	# coupon styling 
	position_bottom = models.CharField(max_length=50, blank=True)

	header_bg_color = models.CharField(max_length=30, blank=True)
	header_text_color = models.CharField(max_length=30, blank=True)
	like_text_color = models.CharField(max_length=30, blank=True)

	background_color = models.CharField(max_length=30, blank=True)

	def __str__(self):
		return self.name

class Coupon(models.Model):
	coupon_code = models.CharField(unique=True, max_length=150)

	customer_fk = models.ForeignKey(Customer, on_delete=models.CASCADE)
	coupon_type = models.ForeignKey(ActiveCoupon, on_delete=models.CASCADE)

	date_created = models.DateTimeField()
	redeemed = models.BooleanField(default=False)
	date_redeemed = models.DateTimeField(null=True, blank=True)
	start_date = models.DateTimeField()
	expires = models.DateTimeField()

	def __str__(self):
		return self.coupon_code 