from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from job_board.models import *
from wmd.widgets import MarkDownInput

class JobForm(ModelForm):
    description = forms.CharField(widget=MarkDownInput(attrs={'cols': 90, 'rows': 15}))
    honeypot    = forms.CharField(required=False,
                                label=_('If you enter anything in this field '\
                                        'your comment will be treated as spam'))

    def clean_honeypot(self):
        """Check that nothing's been entered into the honeypot."""
        value = self.cleaned_data["honeypot"]
        if value:
            raise forms.ValidationError(self.fields["honeypot"].label)
        return value
    
    class Meta:
        model = Job
        fields = ('title', 'category', 'job_type', 'description', 
                  'company_name', 'location',
                  'onsite_required', 'website', 'to_apply')