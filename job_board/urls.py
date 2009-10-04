from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap

from job_board.models import Job
from job_board.feeds import JobFeed
from job_board.forms import JobForm
from job_board.views import JobFormPreview, job_list

from commons.utils import days_range

queryset = Job.objects.filter(posted__gt=days_range(30))

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

sitemaps = {
    'flatpages': FlatPageSitemap,
    'entries': GenericSitemap(job_list_dict, priority=0.6),
}

urlpatterns = patterns('',
    (r'^feed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, 'job-feeds'),
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}, 'job-sitemap'),
    
    (r'^new/$', JobFormPreview(JobForm), {}, 'job-form'),
    (r'^(?P<slug>[\w-]+)/(?P<object_id>\d+)/$', list_detail.object_detail, dict(job_detail_dict), 'job-detail'),
    (r'^tag/(?P<tag_name>[\w-]+)/$', job_list, dict(job_list_dict) ),
    (r'^$', list_detail.object_list, dict(job_list_dict), 'job-list'), # This must be last after everything else has been evaluated
)