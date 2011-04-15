from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from views import *

urlpatterns = patterns('',
    url(r'^post$', post, name="new_posting"),
    url(r'^posting/(?P<id>[\d]+)/$', posting, name="posting"),
    url(r'^delete/(?P<id>[\d]+)/$', delete, name="posting_delete"),
    url(r'^load/(?P<id>[\d]+)/$', load_postings, name="postings_load"),
)
