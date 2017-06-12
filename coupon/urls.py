
from django.conf.urls import url 

from .views import generate, redeem

urlpatterns = [ 
    url(r'^generate/(?P<code>[a-zA-Z0-9_]*)/$', generate, name='generate'), 
    url(r'^redeem/$', redeem, name='redeem'),  
]