from django.conf.urls.defaults import *
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap

from job_board.models import Job
from job_board.feeds import JobFeed
from job_board.forms import JobForm
from job_board.views import JobFormPreview, job_list_by_tag, job_list, job_detail

feeds = {
    'jobs': JobFeed,
}

info_dict = {
    'queryset': Job.objects.filter(),
    'date_field': 'posted'
}

sitemaps = {
    'flatpages': FlatPageSitemap,
    'jobs': GenericSitemap(info_dict, priority=0.6),
}

urlpatterns = patterns('',
    url(r'^feed/(?P<url>.*)/$',
        'django.contrib.syndication.views.feed',
        {'feed_dict': feeds},
        name='job-feeds'),

    url(r'^sitemap.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps},
        name='job-sitemap'),
    
    url(r'^new/$',
        JobFormPreview(JobForm),
        name='job-form'),

    url(r'^(?P<object_id>\d+)/(?P<slug>[\w-]+)/$',
        job_detail,
        name='job-detail'),

    url(r'^tag/(?P<tag_name>[\w-]+)/$',
        job_list_by_tag,
        name='job-list-tag' ),

    url(r'^$',
        job_list,
        name='job-list'), # This must be last after everything else has been evaluated
)