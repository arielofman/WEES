# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Coupon, ActiveCoupon

class CouponModelAdmin(admin.ModelAdmin):
	readonly_fields=('id',)
	search_fields = ["coupon_code"]
	list_filter = ["redeemed", "date_redeemed"]
	class Meta:
		model = Coupon

class ActiveCouponModelAdmin(admin.ModelAdmin):
	readonly_fields=('id',)
	search_fields = ["name"] 
	class Meta:
		model = ActiveCoupon

admin.site.register(ActiveCoupon, ActiveCouponModelAdmin)
admin.site.register(Coupon, CouponModelAdmin)