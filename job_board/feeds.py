from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

from job_board.models import Job
from commons.utils import days_range

class JobFeed(Feed):
    feed_type = Atom1Feed
    title = "Job Feeds"
    link = "/feed/jobs/"
    description = "Job Feeds"
    description_template = 'job_board/feed.html'

    def items(self, obj):
        return Job.objects.filter(posted__gt=days_range(30))

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