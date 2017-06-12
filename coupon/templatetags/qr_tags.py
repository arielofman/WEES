from django import template 

register = template.Library()

@register.inclusion_tag('coupon/qr_tag.html', takes_context=True)
def qr_from_text(context, size='100'):  
	return {"text": context['request'].build_absolute_uri(), "size": size}