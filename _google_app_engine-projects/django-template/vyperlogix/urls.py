from django.conf.urls.defaults import *

from views import default

urlpatterns = patterns('',
                       (r'.*', default.default),
)
