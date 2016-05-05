from django.conf.urls import url
from . import views

# Add your url, corresponding view, and name here

urlpatterns = [
	url(r'^$', views.index, name='root_index'),
	url(r'^browse/$', views.category_default, name="category_default_page"),
	url(r'^browse/(?P<category_id>[0-9]+)/$', views.category_specific, name="category_page"),
	url(r'^protocol/(?P<protocol_id>[0-9]+)/$', views.protocol, name="category_page"),
]
