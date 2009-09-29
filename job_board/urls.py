from django.conf.urls.defaults import *
from django.views.generic import list_detail

from job_board.models import Job
from job_board.feeds import JobFeed
from job_board.forms import JobForm
from job_board.views import JobFormPreview

queryset = Job.objects.all()

feeds = {
    'jobs': JobFeed,
}

job_list_dict = {
    'queryset': queryset,
    'template_name': 'job_board/list.html',
    'template_object_name': 'job',
    'paginate_by': 10,
}

job_detail_dict = {
    'queryset': queryset,
    'template_name': 'job_board/view.html',
    'template_object_name': 'job'
}

urlpatterns = patterns('',
    (r'^feed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, 'job-feeds'),	
    (r'^new/$', JobFormPreview(JobForm), {}, 'job-form'),
    (r'^(?P<slug>[\w-]+)/(?P<object_id>\d+)/$', list_detail.object_detail, dict(job_detail_dict), 'job-detail'),
    (r'^$', list_detail.object_list, dict(job_list_dict), 'job-list'), # This must be last after everything else has been evaluated
)