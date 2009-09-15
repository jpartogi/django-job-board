from django.db import models

TYPE = (
        ('P', 'Permanent'),
        ('C', 'Contract'),
        ('I', 'Internship'),
    )

class Job(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    #notes = models.CharField(max_length=128, null=True)
    posted = models.DateTimeField()
    #closed = models.BooleanField(default=False)
    #closing_date = models.DateField(null=True)
    skills_required = models.TextField(null=True, blank=True)
    #start_date = models.DateField(null=True)
    location = models.CharField(max_length=128)
    #owner = models.ForeignKey('member.ProjectOwner')
    onsite_required = models.BooleanField(default=False)
    #travel_required = models.BooleanField(default=False)
    job_type = models.CharField(max_length=1,choices=TYPE)
    contact_email = models.EmailField()
    contact_person = models.CharField(max_length=128)
    website = models.URLField(null=True, blank=True)
    #year_experience = models.PositiveIntegerField(null=True)
    budget = models.FloatField(null=True, blank=True)
    company_name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/job/%d/" % (self.id)

    class Meta:
        ordering = ['-posted']
        get_latest_by = 'posted'