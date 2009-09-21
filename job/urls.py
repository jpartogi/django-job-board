from django.conf.urls.defaults import *

from job.feeds import JobFeed

feeds = {
    'jobs': JobFeed,
}

urlpatterns = patterns('',
    (r'^$', 'job.views.list', {}, 'job-list'),
	(r'^feed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, 'job-feeds'),
    (r'^add/$', 'job.views.add'),
    (r'^(?P<job_id>\d+)/$', 'job.views.view'),
    (r'^my/$', 'job.views.my_jobs'),
    (r'^edit/(?P<job_id>\d+)/$', 'job.views.edit'),
    #(r'^close/(?P<job_id>\d+)/$', 'close'),
    #(r'^t/(?P<short_name>\S+)/$', 'types'),
    #(r'^tag/(?P<tag_name>\S+)/$', 'tag'),
    #(r'^tag/(?P<skill_name>\S+)/$','tag'),
)