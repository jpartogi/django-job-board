from django.test import TestCase

from job_board.models import Job

class JobTestCase(TestCase):
    fixtures = ['jobs']
    
    def testDisplay30DaysOldJob(self):
        jobs = Job.objects.filter()
        # Should not get any job because it's backdate is more than 30 days old
        self.assert_(len(jobs) == 0)