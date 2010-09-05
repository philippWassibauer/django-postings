from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from views import *

urlpatterns = patterns('',
    url(r'^post$', post, name="new_posting"),
)
