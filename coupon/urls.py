
from django.conf.urls import url 

from .views import generate, code_gate, redeem

urlpatterns = [ 
    url(r'^generate/$', generate, name='generate'), 
    url(r'^codegate/$', code_gate, name='codegate'), 
    url(r'^redeem/(?P<code>[a-zA-Z0-9_]*)/$', redeem, name='redeem'),  
]