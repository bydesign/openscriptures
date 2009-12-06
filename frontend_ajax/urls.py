from django.conf.urls.defaults import *

urlpatterns = patterns('frontend_ajax.views',
	(r'^work/$', 'viewer'),
	(r'^ajax/tok/(?P<work_slug>.+)/(?P<ref_slug>[^/]+)/prev/$', 'ajaxTokPrev'),	#ajax infinite-scroll functionality
	(r'^ajax/tok/(?P<work_slug>.+)/(?P<ref_slug>[^/]+)/next/$', 'ajaxTokNext'), #ajax infinite-scroll functionality
	(r'^ajax/tok/(?P<work_slug>.+)/(?P<ref_slug>[^-]+)-(?P<ref_slug_end>.+)/$', 'ajaxTok'),
	(r'^ajax/tok/(?P<work_slug>.+)/(?P<ref_slug>.+)/$', 'ajaxTok'),
	(r'^ajax/tok-simple/(?P<work_slug>.+)/(?P<ref_slug>.+)/$', 'ajaxTokSimple'),
	(r'^ajax/nav/(?P<work_slug>.+)/books/$', 'ajaxBookNav'),
	(r'^ajax/nav/(?P<work_slug>.+)/(?P<ref_slug>.+)/$', 'ajaxChapterNav'),
)
