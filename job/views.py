from datetime import datetime

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings

from recaptcha.client import captcha

from commons.utils import days_range
from job.models import *
from job.forms import *

def add(request):
    html_captcha = captcha.displayhtml(settings.RECAPTCHA_PUB_KEY)

    if request.method == 'POST':

        check_captcha = captcha.submit(request.POST['recaptcha_challenge_field'], 
                                       request.POST['recaptcha_response_field'],
                                       settings.RECAPTCHA_PRIVATE_KEY, request.META['SERVER_NAME'])
        
	if check_captcha.is_valid is False:
            # Captcha is wrong show an error ...
            request.notifications.create('Captcha challenge is wrong.', 'error')
            
            return HttpResponseRedirect(request.path)

        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.posted = datetime.now()

            job.save()

            request.notifications.create('Your job posting has been saved successfully.', 'success')

            return HttpResponseRedirect('/job/' + str(job.id)) # Redirect after POST

    else:
        form = JobForm()
   
    return render_to_response('job/form.html', {
        'request': request,
        'form': form,
        'html_captcha': html_captcha,
    }, context_instance=RequestContext(request))

def content(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    response = render_to_string('job/content.html', { 'job': job, })

    return HttpResponse(response)

@login_required
@permission_required('project.change_project')
def edit(request, job_id):
    owner = ProjectOwner.objects.get(username=request.session['username'])

    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.posted = datetime.now()
            job.owner = owner

            job.save()

            request.user.message_set.create(message="You have successfully added your job.")

            return HttpResponseRedirect('/job/' + str(job.id) ) # Redirect after POST
    else:
        form = JobForm(instance=job)

    return render_to_response('job/form.html', 
        {'request': request,
         'job': job,
         'form': form,
        },context_instance=RequestContext(request))

@login_required
def my_jobs(request):
    owner =  get_object_or_404(ProjectOwner, username=request.session['username']) # To prevent unauthorized users

    try:
        jobs = Job.objects.all().filter(owner=owner).order_by('-posted')

        paginator = Paginator(jobs, 10)

        # Make sure page request is an int. If not, deliver first page.
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        # If page request (9999) is out of range, deliver last page of results.
        try:
            job_list = paginator.page(page)
        except (EmptyPage, InvalidPage):
            job_list = paginator.page(paginator.num_pages)

    except Job.DoesNotExist:
        jobs = None

    return render_to_response('job/list.html',{'request' : request,
                                               'job_list' : job_list},
                              context_instance=RequestContext(request))

#TODO: view and list can just use generic views
def view(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    return render_to_response('job/view.html', {
        'request' : request,
        'job' : job,
    }, context_instance=RequestContext(request))

def list(request):
    jobs = Job.objects.filter(posted__gt=days_range(30)).order_by('-posted')
    paginator = Paginator(jobs, 10)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        job_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        job_list = paginator.page(paginator.num_pages)

    return render_to_response('job/list.html', {'request' : request,
                                                'job_list' : job_list,},
                              context_instance=RequestContext(request))
