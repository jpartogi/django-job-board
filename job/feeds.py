from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

from job.models import Job
from commons.utils import days_range

class JobFeed(Feed):
    feed_type = Atom1Feed
    title = "Job Feeds"
    link = "/job/"
    description = "Job Feeds"
    description_template = 'job/feed.html'

    def items(self):
        return Job.objects.filter(posted__gt=days_range(30)).order_by('-posted')

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