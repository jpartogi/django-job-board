from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.sitemaps import ping_google
from django.utils.translation import ugettext_lazy as _

from job_board.manager import JobManager
from job_board.signals import view_job
from wmd import models as wmd_models

TYPE = (
        ('P', _('Permanent')),
        ('C', _('Contract')),
        ('I', _('Internship')),
    )

class JobCategory(models.Model):
    name            = models.CharField(max_length=50)
    description     = models.TextField(null=True, blank=True)
    slug            = models.SlugField(max_length=50)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/category/%s/" % ( self.slug )

    class Meta:
        verbose_name_plural = _('categories')
        ordering = ['name']

class Checklist(models.Model):
    question        = models.CharField(max_length=100)

class Job(models.Model):
    title           = models.CharField(max_length=50, verbose_name=_('job title'),
                      help_text=_('job title'))
    slug            = models.SlugField(max_length=50)
    description     = wmd_models.MarkDownField()
    posted          = models.DateTimeField(auto_now_add=True)
    location        = models.CharField(max_length=128, null=True, blank=True, help_text=_('job location'))
    onsite_required = models.BooleanField(default=True)
    job_type        = models.CharField(max_length=1, choices=TYPE)
    category        = models.ForeignKey(JobCategory, verbose_name=_('job category'))
    to_apply        = models.CharField(max_length=128, verbose_name=_('how to apply'),
                      help_text=_('"Send your resume to John Doe (john.doe@company.com)"'))
    website         = models.URLField(verify_exists=False, null=True, blank=True,
                      help_text=_('"www.company.com"'))
    company_name    = models.CharField(max_length=128)
    viewed          = models.IntegerField(editable=False, default=1)
    checklist       = models.ManyToManyField(Checklist, through='JobChecklist')

    objects = JobManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/%d/%s/" % ( self.id, self.slug )

    def save(self):
        self.slug = slugify(self.title)
        super(Job, self).save()
        
        try:
             ping_google()
        except Exception:
             # Bare 'except' because we could get a variety
             # of HTTP-related exceptions.
             pass

    def on_job_view(sender, **kwargs):
        job = kwargs['job']
        job.viewed = job.viewed + 1
        job.save()

    view_job.connect(on_job_view)

    class Meta:
        ordering = ['-posted']
        get_latest_by = 'posted'

class JobChecklist(models.Model):
    checklist       = models.ForeignKey(Checklist)
    job             = models.ForeignKey(Job)
    answer          = models.BooleanField()

    class Meta:
        db_table = 'job_board_job_checklist'