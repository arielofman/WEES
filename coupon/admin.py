# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Coupon

class CouponModelAdmin(admin.ModelAdmin):
	search_fields = ["coupon_code"]
	list_filter = ["redeemed", "date_redeemed"]
	class Meta:
		model = Coupon
 
admin.site.register(Coupon, CouponModelAdmin)