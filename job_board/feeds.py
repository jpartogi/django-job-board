from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed

from job_board.models import Job

class JobFeed(Feed):
    description_template = 'job_board/feed.html'

    def title(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return _("%(site_name)s Job Feed") % dict(site_name=self._site.name)

    def description(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return _("Latest job postings on %(site_name)s") % dict(site_name=self._site.name)
    
    def items(self, obj):
        return Job.objects.filter()

    def item_author_name(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        author's name as a normal Python string.
        """
        return item.company_name

    def item_pubdate(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        pubdate.
        """
        return item.posted

    def link(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return "http://%s/" % (self._site.domain)