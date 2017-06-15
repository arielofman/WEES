# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string

from .models import Coupon
from accounts.models import Customer

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required 

import datetime
from django.utils import timezone

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def create_coupon(customer_obj, coupon_expires):
	coupon_uid = get_random_string(length=23)  
	now = timezone.now()
	Coupon.objects.create(coupon_code=coupon_uid, 
		customer_fk=customer_obj, 
		date_created=now,
		redeemed=False,
		expires=coupon_expires).save() 

	# update refresh to current time 
	setattr(customer_obj, 'refresh', now)
	customer_obj.save()

	return coupon_uid

def generate(request, **kwargs): 
	# the current sessions IP Address
	customer_ip = get_client_ip(request)

	now = timezone.now() 

	coupons = Coupon.objects.select_related('customer_fk').filter(customer_fk__ip_address=customer_ip)
	
	# rate at which customers can generate new coupons
	refresh_rate = datetime.timedelta(hours=24)
	# a set expiration for all coupons
	expiration = now + datetime.timedelta(hours=48)

	# check if customer is in the DB otherwise create new customer
	try:
		customer = Customer.objects.get(ip_address=customer_ip)
	except ObjectDoesNotExist:
		customer = Customer.objects.create(ip_address=customer_ip, refresh=(now-refresh_rate))
		customer.save()  

	try:
		unredeemed = coupons.get(redeemed=False) 
	except ObjectDoesNotExist:
		unredeemed = None
	redeemed = coupons.filter(redeemed=True) 
 
	# NOTE: this method assumes there's only 1 unredeemed coupon per IP
	# if the customer has an unredeemed coupon
	if(unredeemed):
		# if the coupon expired
		if(unredeemed.expires <= now):
			# delete the expired coupon
			unredeemed.delete() 
			# generate a new coupon
			coupon_uid = create_coupon(customer, expiration) 
		# if the coupon didn't expire
		elif(unredeemed.expires > now):
			# give customer back their same coupon 
			coupon_uid = unredeemed.coupon_code 
	# if the customer only has redeemed coupons and no unredemed coupons
	elif(redeemed and not unredeemed):  
		# allow user to generate new coupon after 24 hours
		if((now - customer.refresh) >= refresh_rate):
			coupon_uid = create_coupon(customer, expiration)
		else:
			# redirect user to page saying "Please wait 
			# 24 hours before generating new coupon"
			return render(request, "coupon/used_coupon.html")
	# the customer has no coupons 
	else: 
		coupon_uid = create_coupon(customer, expiration) 
 
	return render(request, "coupon/generate.html", {"code": coupon_uid})
 
def redeem(request, **kwargs):
	# When you redeem coupon, your refresh is set to the date and time u redeemed coupon

	if(request.method == "POST"):
		# check if coupon ID is valid
		try:
			coupon = Coupon.objects.get(coupon_code=kwargs['code'])
		except ObjectDoesNotExist:
			return render(request, "coupon/invalid_coupon.html", {"code": kwargs['code']})
		
		date_created = coupon.date_created
		date_expires = coupon.expires 

		now = timezone.now()
 
		# set the coupon as redeemed
		setattr(coupon, 'redeemed', True)
		setattr(coupon, 'date_redeemed', now)
		coupon.save()

		coupon.customer_fk.refresh = now

		# update when it was redeemed for data
		return render(request, "coupon/redeem.html", {"code": kwargs['code'], "expires":date_expires, "created":date_created})
	
	else:
		# check if coupon ID is valid
		try:
			coupon = Coupon.objects.get(coupon_code=kwargs['code'])
		except ObjectDoesNotExist:
			return render(request, "coupon/invalid_coupon.html", {"code": kwargs['code']})
		
		date_created = coupon.date_created
		date_expires = coupon.expires 

		now = timezone.now()

		# the coupon has already been redeemed
		if(coupon.redeemed):
			date_redeemed = coupon.date_redeemed
			return render(request, "coupon/already_redeemed.html", {"code": kwargs['code'], "expires":date_expires, "created":date_created, "redeemed": date_redeemed})
		# the coupon expired
		elif(date_expires <= now):
			return render(request, "coupon/expired.html", {"code": kwargs['code'], "expires":date_expires, "created":date_created})
		# page to redeem coupon
		else:
			return render(request, "coupon/redeem.html", {"code": kwargs['code'], "expires":date_expires, "created":date_created})
	

	
 