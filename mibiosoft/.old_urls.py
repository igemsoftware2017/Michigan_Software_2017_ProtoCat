
        """
        url(r'^user/password/reset/$', views.password_reset, name="password_reset"),
        url(r'^user/password/reset/done/$', views.password_reset_done, name="password_reset_done"),
        url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
            auth_views.password_reset_confirm, name="password_reset_confirm"),
        url(r'^user/password/done/$', views.password_reset_complete), 
        url(r'^thanks/$', views.thanks, name='thanks'),
        url(r'^invalidemail/$', views.invalid_email, name='invalidemail'),
        """
