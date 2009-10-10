from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.sitemaps import ping_google
from django.utils.translation import ugettext as _

from tagging.models import Tag

TYPE = (
        ('P', _('Permanent')),
        ('C', _('Contract')),
        ('I', _('Internship')),
    )

class JobCategory(models.Model):
    name        = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    slug        = models.SlugField(max_length=50)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/category/%s/" % ( self.slug )

    class Meta:
        verbose_name_plural = _('categories')
        ordering = ['name']
        
class Job(models.Model):
    title           = models.CharField(max_length=50, verbose_name=_('job title'),
                      help_text=_('"Scrum Master" "Senior Rails Developer"'))
    slug            = models.SlugField(max_length=50)
    description     = models.TextField()
    posted          = models.DateTimeField(auto_now_add=True)
    location        = models.CharField(max_length=128, help_text=_('"Sydney, Australia"'))
    onsite_required = models.BooleanField(default=False)
    job_type        = models.CharField(max_length=1, choices=TYPE)
    category        = models.ForeignKey(JobCategory, verbose_name=_('job category'))
    to_apply        = models.CharField(max_length=128, verbose_name=_('how to apply'),
                      help_text=_('"Send your resume to John Doe (john.doe@company.com)"'))
    website         = models.URLField(verify_exists=False, null=True, blank=True,
                      help_text=_('"www.company.com"'))
    company_name    = models.CharField(max_length=128)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/%s/%d/" % ( self.slug, self.id )

    def save(self):
        self.slug = slugify(self.title)
        super(Job, self).save()
        
        try:
             ping_google()
        except Exception:
             # Bare 'except' because we could get a variety
             # of HTTP-related exceptions.
             pass

    def _get_tags(self):
        return Tag.objects.get_for_object(self)

    def _set_tags(self, tag_list):
        Tag.objects.update_tags(self, tag_list)

    tags = property(_get_tags, _set_tags)
    
    class Meta:
        ordering = ['-posted']
        get_latest_by = 'posted'