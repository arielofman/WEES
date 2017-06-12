# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.
def generate(request, **kwargs):
	print(kwargs)
	return render(request, "coupon/generate.html", {"code": kwargs.get('code')})

def redeem(request):
	return render(request, "coupon/redeem.html")