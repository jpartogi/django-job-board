from django import forms
from django.forms import ModelForm

from job_board.models import *

class JobForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 90, 'rows': 15}))
    skills_required = forms.CharField(help_text='Separated by comma')

    class Meta:
        model = Job
        fields = ('title', 'job_type', 'description', 'skills_required',
                  'company_name', 'location', 'onsite_required',
                  'website', 'to_apply')