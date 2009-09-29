from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.formtools.preview import FormPreview

from job_board.models import *
from job_board.forms import *

class JobFormPreview(FormPreview):
    preview_template = 'job_board/preview.html'
    form_template = 'job_board/form.html'
    
    def done(self, request, cleaned_data):
        form = JobForm(cleaned_data)
        job = form.save()
        params = {'slug': job.slug, 'object_id': job.id}
        
        request.notifications.create('Your job posting has been saved successfully. Thank you very much.', 'success')

        return HttpResponseRedirect(reverse('job-detail', kwargs=params))