# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string

from .models import Coupon, ActiveCoupon
from accounts.models import Customer

from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

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

def generate_uid(uid_length, uid_chars): 
	try: 
		while(True):
			coupon_uid = get_random_string(length=uid_length, allowed_chars=uid_chars)
			coupon = Coupon.objects.get(coupon_code=coupon_uid)
	except ObjectDoesNotExist:
		pass

	return coupon_uid

def create_coupon(customer_obj, coupon_obj, coupon_starts, coupon_expires):
	coupon_uid = generate_uid(9, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

	now = timezone.now()
	Coupon.objects.create(coupon_code=coupon_uid, 
		customer_fk=customer_obj,
		coupon_type=coupon_obj,
		date_created=now,
		redeemed=False,
		start_date=coupon_starts,
		expires=coupon_expires).save() 

	# update refresh to current time 
	setattr(customer_obj, 'refresh', now)
	customer_obj.save()

	return coupon_uid

def coupon_list(request):
	active_coupons = ActiveCoupon.objects.all().filter(active=True)

	return render(request, "coupon/coupon_list.html", {"active_coupons": active_coupons})

def generate(request, **kwargs):   
	# get the active coupon object   
	selected_coupon = get_object_or_404(ActiveCoupon, id=kwargs['c_id'])

	# the current sessions IP Address
	customer_ip = get_client_ip(request)
	# current time and date of set timezone
	now = timezone.now() 
	# rate at which customers can generate new coupons
	refresh_rate = datetime.timedelta(hours=12)

	# get all the coupons associated with IP Address
	coupons = Coupon.objects.select_related('customer_fk').filter(customer_fk__ip_address=customer_ip)

	# check if customer is in the DB otherwise create new customer
	try:
		customer = Customer.objects.get(ip_address=customer_ip)
	except ObjectDoesNotExist:
		customer = Customer.objects.create(ip_address=customer_ip, refresh=(now-refresh_rate))
		customer.save()  

	# get all the unredeemed coupons of selected_coupon type
	try:
		unredeemed = coupons.get(Q(coupon_type=selected_coupon), Q(redeemed=False)) 
	except ObjectDoesNotExist:
		unredeemed = None
	except MultipleObjectsReturned:
		# delete all the unredeemed coupons if theres more than one
		coupons.filter(coupon_type=selected_coupon).filter(redeemed=False).delete() 
	# get all the redeemed coupons
	redeemed = coupons.filter(redeemed=True) 

	# data about coupon
	coupon_start = selected_coupon.start_date
	coupon_expires = selected_coupon.expires

	# if the customer has an unredeemed coupon
	if(unredeemed):
		# if the coupon expired
		if(unredeemed.expires <= now):
			# delete the expired coupon
			unredeemed.delete() 
			# generate a new coupon
			coupon_uid = create_coupon(customer, selected_coupon, coupon_start, coupon_expires) 
		# if the coupon didn't expire
		elif(unredeemed.expires > now):
			# give customer back the same coupon 
			coupon_uid = unredeemed.coupon_code 
	# if the customer only has redeemed coupons and no unredemed coupons
	elif(redeemed and not unredeemed):  
		# allow user to generate new coupon after 24 hours
		if((now - customer.refresh) >= refresh_rate):
			coupon_uid = create_coupon(customer, selected_coupon, coupon_start, coupon_expires) 
		else: 
			# if user already redeemed coupon, they have to wait
			# until tomorrow before they can generate a new coupon
			return render(request, "coupon/used_coupon.html")
	# the customer has no coupons 
	else: 
		coupon_uid = create_coupon(customer, selected_coupon, coupon_start, coupon_expires) 

	return render(request, "coupon/generate.html", {"code": coupon_uid, "coupon": selected_coupon})


@login_required(login_url='/error/', redirect_field_name=None)
def code_gate(request, **kwargs):
	return render(request, "coupon/code_gate.html")


@login_required(login_url='/error/', redirect_field_name=None)
def redeem(request, **kwargs):
	# check if coupon code is valid
	try:
		coupon = Coupon.objects.get(coupon_code=kwargs['code'])

		# get the data about coupon for template
		date_created = coupon.date_created
		date_started = coupon.start_date
		date_expires = coupon.expires 

		now = timezone.now() 

	except ObjectDoesNotExist:
		return render(request, "coupon/invalid_coupon.html", {"code": kwargs['code']})

	if(request.method == "POST"):  
		# set the coupon as redeemed
		coupon.redeemed = True
		# set the date redeemed to current time
		coupon.date_redeemed = now
		coupon.save() 

		# When you redeem coupon, your refresh is set to the date and time you redeemed coupon
		coupon.customer_fk.refresh = now
		coupon.customer_fk.save()

		return render(request, "coupon/redeem.html", {"code": kwargs['code'], "expires":date_expires, "created":date_created})
	else:  
		context = {
			"code": kwargs['code'],
			"expires":date_expires, 
			"started":date_started, 
			"created":date_created
		}

		if(coupon.redeemed):
			date_redeemed = coupon.date_redeemed
			context.update({"redeemed": date_redeemed})

			return render(request, "coupon/already_redeemed.html", context)
		# the coupon isn't active yet
		elif(date_started > now):
			return render(request, "coupon/not_active.html", context)
		# the coupon expired
		elif(date_expires <= now):
			return render(request, "coupon/expired.html", context)
		# page to redeem coupon
		else:
			return render(request, "coupon/redeem.html", context)

			