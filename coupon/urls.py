
from django.conf.urls import url 

from .views import generate, redeem

urlpatterns = [ 
    url(r'^generate/$', generate, name='generate'), 
    url(r'^redeem/$', redeem, name='redeem'),  
]