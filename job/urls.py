from django.conf.urls.defaults import *
from django.views.generic import date_based, list_detail, simple

from job.models import Job
from job.feeds import JobFeed

queryset = Job.objects.all()

feeds = {
    'jobs': JobFeed,
}

job_list_dict = {
    'queryset': queryset,
    'template_name': 'job/list.html',
    'template_object_name': 'job',
    'paginate_by': 10,
}

job_detail_dict = {
	'queryset': queryset,
	'template_name': 'job/view.html',
    'template_object_name': 'job'
}

urlpatterns = patterns('',
	(r'^feed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, 'job-feeds'),
	
    #(r'^add/$', 'job.views.add'),
    #(r'^my/$', 'job.views.my_jobs'),
    #(r'^edit/(?P<job_id>\d+)/$', 'job.views.edit'),
	
    #(r'^close/(?P<job_id>\d+)/$', 'close'),
    #(r'^t/(?P<short_name>\S+)/$', 'types'),
    #(r'^tag/(?P<tag_name>\S+)/$', 'tag'),
    #(r'^tag/(?P<skill_name>\S+)/$','tag'),
	
    (r'^(?P<slug>[\w-]+)/(?P<object_id>\d+)/$', list_detail.object_detail, dict(job_detail_dict), 'job-detail'),
    (r'^$', list_detail.object_list, dict(job_list_dict), 'job-list'), # This must be last after everything else has been evaluated
)