from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.loader import select_template
from django.contrib.formtools.preview import FormPreview
from django.views.generic import list_detail
from django.shortcuts import render_to_response

from commons.search import get_query

from job_board.models import *
from job_board.forms import *
from job_board.signals import view_job

queryset = Job.objects.filter()

template_object_name = 'job'

extra_context = {'base_template' : 'base.html'}

job_list_template = (
    "job_board/list.html",
    "job_board/job_list.html",
)

def job_list(request):
    template = select_template(job_list_template) # returns Template object
    template_name = template.name

    paginate_by = 10
    
    return list_detail.object_list(request, queryset,
                                    paginate_by = paginate_by,
                                    template_name = template_name,
                                    extra_context = extra_context,
                                    template_object_name = template_object_name)
    
def job_search(request):
    query_string = ''
    job_list = None

    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        query = get_query(query_string, ['title', 'location', 'description'])

        job_list = Job.objects.filter(query).order_by('-posted')

    template = select_template(job_list_template) # returns Template object
    template_name = template.name

    extra_context['query_string'] = query_string
    extra_context['job_list'] = job_list
    
    return render_to_response(template_name, extra_context, context_instance=RequestContext(request))


def job_detail(request, slug=None, object_id=None):
    job_detail_template = (
        "job_board/view.html",
        "job_board/detail.html",
        "job_board/job_detail.html",
    )
    
    template = select_template(job_detail_template)
    template_name = template.name

    job = Job.objects.get(pk=object_id)
    view_job.send(sender=job_detail, job=job)

    return list_detail.object_detail(request, queryset,
                                     object_id = object_id,
                                     slug = slug,
                                     template_name = template_name,
                                     extra_context = extra_context,
                                     template_object_name = template_object_name)     

class JobFormPreview(FormPreview):
    preview_template = 'job_board/preview.html'
    form_template = 'job_board/form.html'
        
    def done(self, request, cleaned_data):
        form = JobForm(request.POST)
        job = form.save()

        message = """Your job posting has been saved successfully. Thank you very much.
        """

        request.notifications.create(message, 'success')

        params = {'slug': job.slug, 'object_id': job.id}
        return HttpResponseRedirect(reverse('job-detail', kwargs=params))