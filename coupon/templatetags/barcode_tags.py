from django import template  
from django.urls import reverse

register = template.Library()

@register.inclusion_tag('coupon/barcode_tag.html', takes_context=True)
def bc_from_text(context):    
	barcode = context['code']
	return {"barcode": barcode}

@register.simple_tag(takes_context=True) 
def barcode_text(context): 
	return context['code']