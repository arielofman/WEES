from django import template  
from django.urls import reverse

register = template.Library()

@register.inclusion_tag('coupon/qr_tag.html', takes_context=True)
def qr_from_text(context, size='100'):    
	redeem_url = context['request'].build_absolute_uri(reverse('redeem', kwargs={'code': context['code']}))
	return {"code_url": redeem_url, "size": size}

@register.simple_tag(takes_context=True) 
def qr_code_text(context): 
	return context['code']