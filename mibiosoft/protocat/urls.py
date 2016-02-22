from django.conf.urls import url
from . import views

# Add your url, corresponding view, and name here

urlpatterns = [
    url(r'^$', views.index, name='root_index'),
]