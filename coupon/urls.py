
from django.conf.urls import url 

from .views import generate, coupon_list, code_gate, redeem

urlpatterns = [ 
    url(r'^(?P<c_id>[0-9_]+)/$', generate, name='generate'), 
    url(r'^list/$', coupon_list, name='generate'), 
    url(r'^codegate/$', code_gate, name='codegate'), 
    url(r'^redeem/(?P<code>[a-zA-Z0-9_]*)/$', redeem, name='redeem'),  
]