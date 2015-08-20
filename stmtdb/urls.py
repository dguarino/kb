"""stmtdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_change, password_change_done
#from django.conf import settings

# admin
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
	#url( r'^knowledgebase/$', 'django.contrib.auth.views.login'),
	url( r'^knowledgebase/login/$', 'django.contrib.auth.views.login'),
	url( r'^knowledgebase/password/change/$', 'django.contrib.auth.views.password_change'),
	url( r'^knowledgebase/password/change/done$', 'django.contrib.auth.views.password_change_done'),
	url( r'^knowledgebase/logout$', 'maps.views.logout_page' ),

    url( r'^knowledgebase/$', 'maps.views.home' ),
	url( r'^knowledgebase/help$', 'maps.views.help' ),

	url( r'^knowledgebase/questions/$', 'maps.views.stmt_requests' ),
	url( r'^knowledgebase/questions/add$', 'maps.views.stmt_requests_add' ),
	url( r'^knowledgebase/questions/edit$', 'maps.views.stmt_requests_edit' ),

	url( r'^knowledgebase/map/$', 'maps.views.map' ),
	url( r'^knowledgebase/map/add$', 'maps.views.add' ),
	url( r'^knowledgebase/map/edit$', 'maps.views.edit' ),
	url( r'^knowledgebase/map/delete$', 'maps.views.delete' ),
	url( r'^knowledgebase/map/statement/(?P<stmt_id>\d+)/$', 'maps.views.highlight_stmt' ),
	url( r'^knowledgebase/map/evidence/(?P<evdc_id>\d+)/$', 'maps.views.highlight_evdc' ),
	url( r'^knowledgebase/map/article/(?P<artl_id>\d+)/$', 'maps.views.highlight_artl' ),

	url( r'^knowledgebase/detail/(?P<entity>[a-z]+)/(?P<ntt_id>\d+)/$', 'maps.views.detail' ),

	url( r'^knowledgebase/upload$', 'maps.views.upload_bibtex' ),
	url( r'^knowledgebase/export$', 'maps.views.export_csv' ),

	url( r'^knowledgebase/comments/post/', 'maps.views.comment_post_wrapper' ),
	url( r'^knowledgebase/comments/', include('django_comments.urls') ),

	url( r'^knowledgebase/admin/', include(admin.site.urls) ),
)
