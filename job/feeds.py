from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

from djobb.models import Job
from djobb.utils import thirty_days_range

class LatestJobs(Feed):
    feed_type = Atom1Feed
    title = "Jobs Feed"
    link = "/job/"
    description = "Jobs Feed"
    description_template = 'job/feed.html'

    def items(self):
        return Job.objects.filter(posted__gt=thirty_days_range()).order_by('-posted')

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