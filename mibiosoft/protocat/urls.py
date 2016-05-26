from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

# Add your url, corresponding view, and name here

urlpatterns = [
	url(r'^$', views.index, name='root_index'),
	url(r'^signup/$', views.sign_up, name="sign_up_page"),
	url(r'^submitsignup/$', views.submit_sign_up, name="submit_page"),
	url(r'^login/$', views.login_user, name="login_page"),
	url(r'^submitlogin/$', views.submit_login, name="submit_login_page"),
	url(r'^logoff/$', views.logoff, name="redirect_page"),
	url(r'^reagent/(?P<reagent_id>[0-9]+)/$', views.reagent, name="reagent_page"),
	url(r'^browse/$', views.category_default, name="category_default_page"),
	url(r'^browse/(?P<category_id>[0-9]+)/$', views.category_specific, name="category_page"),
	url(r'^protocol/(?P<protocol_id>[0-9]+)/$', views.protocol, name="category_page"),
	url(r'^user/(?P<user_id>[0-9]+)/$', views.user, name="user_page"),
	url(r'^about/$', views.about, name="about_page"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
