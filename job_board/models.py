from django.db import models
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from django.contrib.sitemaps import ping_google

from tagging.models import Tag

TYPE = (
        ('P', 'Permanent'),
        ('C', 'Contract'),
        ('I', 'Internship'),
    )

class Job(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('job title'))
    slug = models.SlugField(max_length=50)
    description = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)
    skills_required = models.CharField(max_length=100)
    location = models.CharField(max_length=128)
    onsite_required = models.BooleanField(default=False)
    job_type = models.CharField(max_length=1, choices=TYPE)
    to_apply = models.CharField(max_length=128)
    website = models.URLField(verify_exists=False, null=True, blank=True)
    company_name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/%s/%d/" % ( self.slug, self.id )

    def save(self):
        self.slug = slugify(self.title)
        super(Job, self).save()

        self.tags = self.skills_required
        
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