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
	url(r'^editreagent/(?P<reagent_id>[0-9]+)/$', views.edit_reagent, name="edit_reagent_page"),
	url(r'^newreagent/$', views.new_reagent, name="new_reagent_page"),
	url(r'^browse/$', views.category_default, name="category_default_page"),
	url(r'^browse/(?P<category_id>[0-9]+)/$', views.category_specific, name="category_page"),
	url(r'^protocol/(?P<protocol_id>[0-9]+)/$', views.protocol, name="category_page"),
	url(r'^user/(?P<user_id>[0-9]+)/$', views.user, name="user_page"),
	url(r'^about/$', views.about, name="about_page"),
	url(r'^search/$', views.search, name="about_page"),
	url(r'^rating/$', views.submit_rating, name="ajax_rating"),
	url(r'^upload/$', views.upload_default, name="default_upload_page"),
	url(r'^upload/(?P<protocol_id>[0-9]+)/$', views.upload_branch, name="upload_page"),
	url(r'^submitprotocol/$', views.submit_upload, name="submit_upload_page"),
	url(r'^toggleprotocol/$', views.toggle_protocol, name="toggle_page"),
	url(r'^submitcomment/$', views.submit_comment, name="submit_comment_page"),
	url(r'^updateprofile/$', views.update_profile, name="update_profile"),
	url(r'^getcategoryprotocols/(?P<category_id>[0-9]*)/$', views.get_protocols_from_category, name="update_profile"),
	url(r'^test/$', views.test, name="test"),
	url(r'^github/$', views.github, name="github"),
	url(r'^postgithub/$', views.github_post, name="githubpost"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
