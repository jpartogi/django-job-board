from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.formtools.preview import FormPreview
from django.shortcuts import get_object_or_404
from django.views.generic import list_detail

from tagging.models import Tag, TaggedItem

from job_board.models import *
from job_board.forms import *

def job_list(request, tag_name=None, queryset=None, paginate_by=None,
        template_name=None, template_object_name=None):

    if tag_name != None:
        tag = get_object_or_404(Tag,name=tag_name)
        #queryset = TaggedItem.objects.get_by_model(Entry, tag) #TODO:  this causes bug
        queryset = queryset.filter(skills_required__contains = tag_name) #temporary fix?

    queryset.order_by('posted')
    
    return list_detail.object_list(request, queryset, paginate_by=paginate_by,
                                    template_name = template_name,
                                    template_object_name= template_object_name)

class JobFormPreview(FormPreview):
    preview_template = 'job_board/preview.html'
    form_template = 'job_board/form.html'
    
    def done(self, request, cleaned_data):
        form = JobForm(cleaned_data)
        job = form.save()
        params = {'slug': job.slug, 'object_id': job.id}
        
        request.notifications.create('Your job posting has been saved successfully. Thank you very much.', 'success')

        return HttpResponseRedirect(reverse('job-detail', kwargs=params))