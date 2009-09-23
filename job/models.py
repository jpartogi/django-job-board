from django.db import models

TYPE = (
        ('P', 'Permanent'),
        ('C', 'Contract'),
        ('I', 'Internship'),
    )

class Job(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)
    skills_required = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=128)
    #owner = models.ForeignKey('member.ProjectOwner')
    onsite_required = models.BooleanField(default=False)
    job_type = models.CharField(max_length=1,choices=TYPE)
    contact_email = models.EmailField()
    contact_person = models.CharField(max_length=128)
    website = models.URLField(null=True, blank=True)
    budget = models.FloatField(null=True, blank=True)
    company_name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/%s/%d/" % ( self.slug, self.id )

    class Meta:
        ordering = ['-posted']
        get_latest_by = 'posted'