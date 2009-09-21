from django.conf.urls.defaults import *

urlpatterns = patterns('job.views',
    (r'^$', 'list'),
    (r'^add/$', 'add'),
    (r'^(?P<job_id>\d+)/$', 'view'),
    (r'^my/$', 'my_jobs'),
    (r'^edit/(?P<job_id>\d+)/$', 'edit'),
    #(r'^close/(?P<job_id>\d+)/$', 'close'),
    #(r'^t/(?P<short_name>\S+)/$', 'types'),
    #(r'^tag/(?P<tag_name>\S+)/$', 'tag'),
    #(r'^tag/(?P<skill_name>\S+)/$','tag'),
)