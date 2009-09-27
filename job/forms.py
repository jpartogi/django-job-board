from django import forms
from django.forms import ModelForm

from job.models import *

class JobForm(ModelForm):
    skills_required = forms.CharField(help_text='A comma separated value of skills. e.g: Java, Linux, Postgres',
                            required=False,
                            widget=forms.Textarea(attrs={'rows':'5'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 90, 'rows': 15}))
    location = forms.CharField(help_text='"Jakarta, Indonesia" or "Boston, MA" or "Sydney, NSW"')

    class Meta:
        model = Job
        fields = ('title', 'job_type', 'description', 'skills_required',
                  'company_name', 'location', 'onsite_required',
                  'website', 'contact_person', 'contact_email')