from django import forms
from django.forms import ModelForm

from job.models import *

class JobForm(ModelForm):
    title = forms.CharField(label = 'Title', help_text='"Senior Java Programmer" or "Web Designer"',
                            widget=forms.TextInput(attrs={'size': 40}))
    skills_required = forms.CharField(help_text='A comma separated value of skills. e.g: Java, Linux, Postgres',
                            required=False,
                            widget=forms.Textarea(attrs={'rows':'5'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 90, 'rows': 15}))
    job_type = forms.CharField(widget=forms.RadioSelect(choices=TYPE))
    location = forms.CharField(help_text='"Jakarta, Indonesia" or "Boston, MA" or "Sydney, NSW"')
    budget = forms.CharField(help_text = 'The budget for salary', required=False)

    class Meta:
        model = Job
        fields = ('title', 'job_type', 'description', 'skills_required',
                  'budget',
                  'company_name', 'location', 'onsite_required',
                  'website', 'contact_person', 'contact_email')