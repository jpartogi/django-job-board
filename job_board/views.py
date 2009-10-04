from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.loader import select_template
from django.contrib.formtools.preview import FormPreview
from django.shortcuts import get_object_or_404
from django.views.generic import list_detail

from tagging.models import Tag, TaggedItem

from commons.utils import days_range

from job_board.models import *
from job_board.forms import *

queryset = Job.objects.filter(posted__gt=days_range(30))

job_list_template = (
    "job_board/list.html",
    "job_board/job_list.html",
)

paginate_by = 10
template_object_name = 'job'

def job_list_by_tag(request, tag_name=None):

    tag = get_object_or_404(Tag,name=tag_name)
    queryset = TaggedItem.objects.get_by_model(Job, tag)

    queryset.order_by('posted')

    template = select_template(job_list_template) # returns Template object
    template_name = template.name

    return list_detail.object_list(request, queryset, paginate_by=paginate_by,
                                    template_name = template_name,
                                    template_object_name= template_object_name)

def job_list(request):
    template = select_template(job_list_template) # returns Template object
    template_name = template.name
    
    return list_detail.object_list(request, queryset, paginate_by=paginate_by,
                                    template_name = template_name,
                                    template_object_name= template_object_name)

def job_detail(request, slug=None, object_id=None):
    job_detail_template = (
        "job_board/view.html",
        "job_board/detail.html",
        "job_board/job_detail.html",
    )

    template = select_template(job_detail_template)
    template_name = template.name

    return list_detail.object_detail(request, queryset, object_id=object_id, slug=slug,
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